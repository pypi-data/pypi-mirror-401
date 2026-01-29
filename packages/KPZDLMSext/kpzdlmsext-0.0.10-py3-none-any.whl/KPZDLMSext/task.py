from copy import copy, deepcopy
from typing import Optional, Self
import re
import asyncio
from dataclasses import dataclass, field
import sqlite3
from StructResult import result
from DLMS_SPODES.obis import media_id
from DLMS_SPODES.types import cdt
from DLMS_SPODES.firmwares import get_firmware
from DLMS_SPODES.cosem_interface_classes.parameter import Parameter
from DLMS_SPODES.cosem_interface_classes import parameters as dlms_par
from DLMS_SPODES.cosem_interface_classes.implementations.data import AFEOffsets, AFERegister
from DLMS_SPODES.cosem_interface_classes.image_transfer import image_transfer_status as i_t_status
from DLMS_SPODES.pardata import ParValues
from DLMS_SPODES_client.logger import LogLevel as logL
from DLMS_SPODES_client.client import Client
from DLMS_SPODES_client import task
from DLMS_SPODES import exceptions as exc
from DLMS_SPODES.pardata import ParData
from SPODESext.parameters import DEVICE_TYPE
from semver import Version as SemVer
from .enums import Command, Status
from .parameters import CALIBRATE, AFE_OFFSETS
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from DLMS_SPODES.cosem_interface_classes.image_transfer.ver0 import ImageToActivateInfo
    from DLMS_SPODES.cosem_interface_classes.register import Register


@dataclass
class RTCOffsetSet(task.SimpleCopy, task.OK):
    db_name: str
    msg: str = "Установка смещения кварца"
    n_phases: str = field(init=False)

    async def exchange(self, c: Client) -> result.Ok | result.Error:
        dev_type: media_id.DeviceIdObjects.TYPE
        self.n_phases = str(c.objects.get_n_phases())
        # descriptor =
        match str(c.objects.firmwares_description.value).split("_", maxsplit=5):
            case _, _, phases_amount, cpu_type, *_:
                if phases_amount[0] in ("1", "3"):
                    self.n_phases = phases_amount[0]
                else:
                    return result.Error.from_e(ValueError(F"Wrong {phases_amount=}"))
            case _:
                raise ValueError(F"Wrong device description: {c.objects.firmwares_description.value}")
        if (data := c.objects.par2data(DEVICE_TYPE.value).unwrap()) is None:
            if isinstance((res_ := await task.Par2Data[media_id.DeviceIdObjects.TYPE](DEVICE_TYPE.value).exchange(c)), result.Error):
                return res_
            dev_type = res_.value
        else:
            dev_type = data
        match dev_type.to_str().split("_", maxsplit=1):
            case "M2M", dev_type:
                match tuple(dev_type):
                    case self.n_phases, :
                        execution_type = "P"
                    case self.n_phases, "S" | "T" | "C" as execution_type:
                        pass
                    case self.n_phases, *wrong_execution_type:
                        return result.Error.from_e(ValueError(f"Phase amount OK. But {wrong_execution_type=}"))
                    case phase_amount_error, _:
                        return result.Error.from_e(ValueError(f"{phase_amount_error=} from device type is different in description object"))
                    case _:
                        return result.Error.from_e(ValueError(f"Wrong {dev_type=}"))
            case _:
                return result.Error.from_e(ValueError(f"Wrong object value device type {DEVICE_TYPE.value}"))
        # set rtc offset
        # db connect
        with sqlite3.connect(self.db_name, timeout=5) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            res = cursor.execute(
                "SELECT rtc_offset FROM RtcOffset WHERE phases_amount = ? AND execution_type = ? AND cpu = ?",
                (int(self.n_phases), execution_type, cpu_type))
            match res.fetchone():
                case sqlite3.Row() as row:
                    rtc_offset: int = row["rtc_offset"]
                case None:
                    return result.Error.from_e(ValueError("Для данной конфигурации не найдено смещение часового кварца"))
                case _ as value:
                    return result.Error.from_e(ValueError(F"Wrong {value}"))
        return await task.WriteTranscript(Parameter.parse("128.0.9.0.0.255:2"), str(rtc_offset)).exchange(c)


@dataclass
class Calibrate(task.SimpleCopy, task.Simple[list[Parameter]]):
    commands: tuple[Command, ...] = (Command.CALIBRATE_ALL,)
    timeout: int = 10
    msg: str = "Калибровка"

    async def exchange(self, c: Client) -> result.Simple[list[Parameter]] | result.Error:
        match c.objects.get_n_phases():
            case 1:
                registers = [
                    Parameter.parse("1.0.9.7.0.255:2"),
                    Parameter.parse("1.0.1.7.0.255:2"),
                    Parameter.parse("1.0.3.7.0.255:2"),
                    Parameter.parse("1.0.12.7.0.255:2"),
                    Parameter.parse("1.0.11.7.0.255:2")
                ]
            case 3:
                registers = [
                    Parameter.parse("1.0.29.7.0.255:2"),
                    Parameter.parse("1.0.21.7.0.255:2"),
                    Parameter.parse("1.0.23.7.0.255:2"),
                    Parameter.parse("1.0.32.7.0.255:2"),
                    Parameter.parse("1.0.31.7.0.255:2"),
                    Parameter.parse("1.0.49.7.0.255:2"),
                    Parameter.parse("1.0.41.7.0.255:2"),
                    Parameter.parse("1.0.43.7.0.255:2"),
                    Parameter.parse("1.0.52.7.0.255:2"),
                    Parameter.parse("1.0.51.7.0.255:2"),
                    Parameter.parse("1.0.69.7.0.255:2"),
                    Parameter.parse("1.0.61.7.0.255:2"),
                    Parameter.parse("1.0.63.7.0.255:2"),
                    Parameter.parse("1.0.72.7.0.255:2"),
                    Parameter.parse("1.0.71.7.0.255:2")
                ]
            case _:
                return result.Error.from_e(ValueError("get_n_phases wrong"))
        if isinstance((res_firmver := await task.GetFirmwareVersion().exchange(c)), result.Error):
            return res_firmver
        if cdt.encoding2semver(res_firmver.value.encoding) < SemVer(1, 3, 19):
            self.commands = (Command.CALIBRATE_A, Command.CALIBRATE_B, Command.CALIBRATE_C)
        if isinstance((res_set_factory := await task.WriteTranscript(CALIBRATE.value, str(Command.SET_FACTORY)).exchange(c)), result.Error):
            return res_set_factory
        for command in self.commands:
            if isinstance((res := await ExecuteCalibrateCommand(command, self.timeout).exchange(c)), result.Error):
                return res
        for register in registers:
            await task.Par2Data(register).exchange(c)
            if not c.objects.par2su(register):
                await task.Par2Data(register.set_i(3)).exchange(c)
        return result.Simple(value=registers)


@dataclass
class ExecuteCalibrateCommand(task.SimpleCopy, task.Simple[int]):
    command: Command
    timeout: int = 20
    msg: str = "Исполнение команды калибровки"

    async def exchange(self, c: Client) -> result.Simple[int] | result.Error:
        if isinstance((res1 := await task.WriteParValue(ParValues(CALIBRATE.value, str(self.command))).exchange(c)), result.Error):
            return res1
        for _ in range(self.timeout):
            await asyncio.sleep(1)
            # return result.Simple(int(Status.COMPLETE))  # for debug
            if isinstance((res2 := (await task.Par2Data[cdt.Digital](CALIBRATE.value).exchange(c))), result.Error):
                return res2
            match int(res2.value):  # todo: make with DLMS typing
                case Status.COMPLETE as ret:
                    return result.Simple(int(ret))
                case Status.BUSY:
                    """wait"""
                case err:
                    return result.Simple(int(err)).append_e(exc.ITEApplication("ошибка калибровки"))
        else:
            return result.Error.from_e(exc.ITEApplication("Неполучен статус ГОТОВО"))


@dataclass
class AFEOffsetsSet(task.SimpleCopy, task.OK):
    db_name: str
    msg: str = "Установка смещений AFE"

    async def exchange(self, c: Client) -> result.Ok | result.Error:
        if isinstance((res := await task.Par2Data[AFEOffsets](AFE_OFFSETS.value).exchange(c)), result.Error):
            return res
        if not isinstance(res.value, AFEOffsets):
            return result.Error.from_e(ValueError(f"got value type {res.value}, expected {AFEOffsets}"))
        with (sqlite3.connect(self.db_name, timeout=5) as conn):
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            values = {name: (value, n) for name, value, n in cursor.execute(
                "SELECT o.name, AVG(o.value) AS average_value, COUNT(*) AS record_count "
                "FROM AFEOffsets o "
                "JOIN AFEs a ON o.LDN = a.LDN "
                "WHERE a.identifier = ? "
                "GROUP BY o.name "
                "ORDER BY o.name;",
                (str(res.value.identifier),)
            ).fetchall()}
            new_offsets: AFEOffsets = copy(res.value)
            for register in new_offsets.register_list:
                if (val := values.get(name := str(register.name))) is None:
                    return result.Error.from_e(ValueError(f"{register.name} is absent in db"))
                value, n = val
                if n < 10:
                    return result.Error.from_e(ValueError(f"the sample: <{name}>={n} is small"))
                new_reg: AFERegister = copy(register)
                if not isinstance(new_reg.value, (cdt.Digital, cdt.Float)):
                    return result.Error.from_e(ValueError(f"{register.name} has wrong type: {register.value}"))
                register.value.set(value)
        await task.WriteParDatas([ParData(AFE_OFFSETS.value, new_offsets)]).exchange(c)
        return result.OK


@dataclass
class CheckAFEOffsets(task.SimpleCopy, task.OK):
    msg: str = "Проверка наличия калибровки офсетов"

    async def exchange(self, c: Client) -> result.Ok | result.Error:
        reg: Register
        if isinstance((res := await task.Par2Data[AFEOffsets](AFE_OFFSETS.value).exchange(c)), result.Error):
            return res
        result_: list[int | float] = []
        for reg in res.value.register_list:
            if isinstance(reg.value, cdt.Float):
                result_.append(float(reg.value))
            else:
                result_.append(int(reg.value))
        if any(result_):
            return result.OK
        return result.Error.from_e(RuntimeError(), msg="Требуется калибровка офсетов. Все AFE регистры пусты")


@dataclass
class ImageTransferOld(task.ImageTransfer):
    async def exchange(self, c: Client) -> result.StrictOk | result.Error:
        res_block_size: result.SimpleOrError[cdt.DoubleLongUnsigned]
        res = result.StrictOk()
        if isinstance(res_block_size := await task.Par2Data(self.par.image_block_size).exchange(c), result.Error):
            return res_block_size
        block_size = int(res_block_size.value)
        self.n_blocks, mod = divmod(len(self.image), block_size)
        if mod != 0:
            self.n_blocks += 1
        if isinstance(res_initiate := await task.Execute2(self.par.image_transfer_initiate, self.ITI).exchange(c), result.Error):
            return res_initiate
        c.log(logL.INFO, "Start initiate Image Transfer")
        while self.n_t_b < self.n_blocks:   # todo copypast from TransferImage
            offset = self.n_t_b * block_size
            if isinstance(res_tr_block := await task.TransferBlock(
                    par=self.par,
                    number=cdt.DoubleLongUnsigned(self.n_t_b),
                    value=cdt.OctetString(bytearray(self.image[offset: offset + block_size]))
            ).exchange(c), result.Error):
                return res_tr_block
            self.n_t_b += 1  # todo: maybe get from SERVER - await get_not_transferred_block.exchange(c)
        c.log(logL.INFO, "All blocks transferred")
        if isinstance(res_initiate := await task.ActivateImage(self.par).exchange(c), result.Error):
            return res_initiate
        c.log(logL.INFO, "Start Activate Transfer, without verification")
        return res


@dataclass
class ImageTransferOld2(task.ImageTransfer):
    async def exchange(self, c: Client) -> result.StrictOk | result.Error:
        res_block_size: result.SimpleOrError[cdt.DoubleLongUnsigned]
        res_status: result.SimpleOrError[i_t_status.ImageTransferStatus]
        res_activate_info: result.SimpleOrError[ImageToActivateInfo]
        res_ntb: result.SimpleOrError[cdt.DoubleLongUnsigned]
        res = result.StrictOk()
        if isinstance(res_block_size := await task.Par2Data(self.par.image_block_size).exchange(c), result.Error):
            return res_block_size
        block_size = int(res_block_size.value)
        # TODO: copypast from TransferImage
        self.n_blocks, mod = divmod(len(self.image), block_size)
        if mod != 0:
            self.n_blocks += 1
        if isinstance(res_ntb := await task.Par2Data(self.par.image_first_not_transferred_block_number).exchange(c), result.Error):
            return res_ntb
        if isinstance(res_status := await task.Par2Data(self.par.image_transfer_status).exchange(c), result.Error):
            return res_status
        if isinstance(res_activate_info := await task.Par2Data(self.par.image_to_activate_info).exchange(c), result.Error):
            return res_activate_info
        if (
            res_status.value in (i_t_status.TRANSFER_NOT_INITIATED, i_t_status.VERIFICATION_FAILED, i_t_status.ACTIVATION_FAILED)
            or len(res_activate_info.value) == 0
            or res_activate_info.value[0].image_to_activate_identification != self.ITI.image_identifier
        ):
            if isinstance(res_initiate := await task.Execute2(self.par.image_transfer_initiate, self.ITI).exchange(c), result.Error):
                return res_initiate
            c.log(logL.INFO, "Start initiate Image Transfer")
        else:
            c.log(logL.INFO, "already INITIATED")
            if isinstance(res_ntb := await task.Par2Data(self.par.image_first_not_transferred_block_number).exchange(c), result.Error):
                return res_ntb
            self.n_t_b = int(res_ntb.value)
            if self.n_t_b == 1:  # bag in SERVER: always start from 1
                self.n_t_b = 0
        while self.n_t_b < self.n_blocks:
            offset = self.n_t_b * block_size
            if isinstance(res_tr_block := await task.TransferBlock(
                    par=self.par,
                    number=cdt.DoubleLongUnsigned(self.n_t_b),
                    value=cdt.OctetString(bytearray(self.image[offset: offset + block_size]))
            ).exchange(c), result.Error):
                return res_tr_block
            self.n_t_b += 1  # todo: maybe get from SERVER - await get_not_transferred_block.exchange(c)
        c.log(logL.INFO, "All blocks transferred")
        if isinstance(res_initiate := await task.ActivateImage(self.par).exchange(c), result.Error):
            return res_initiate
        c.log(logL.INFO, "Start Activate Transfer. Timeout 22 second. Waiting verification")
        if isinstance(res_disconnect := await task.HardwareDisconnect("expected reboot server after upgrade").exchange(c), result.Error):
            return res_disconnect
        await asyncio.sleep(22)
        if isinstance(res_dummy := await task.Dummy().run(c), result.Error):
            return res_dummy
        return res


firm_id_pat = re.compile(b".*(?P<fid>PWRM_M2M_[^_]{1,10}_[^_]{1,10}).+")
boot_ver_pat = re.compile(b"(?P<boot_ver>\\d{1,4}).+")


@dataclass
class UpdateFirmware(task.Subtasks[task.ImageTransfer], task.OK):
    """only for KPZ now, return version in cdt"""
    msg: str = ""
    _current: list[task.ImageTransfer] = field(init=False, default_factory=list)
    find_ver: Optional[SemVer] = field(init=False, default=None)
    """finded version on Client"""
    tasks: list[task.ImageTransfer] = field(init=False, default_factory=list)

    def copy(self) -> Self:
        return deepcopy(self)

    @property
    def current(self) -> Self | task.ImageTransfer:
        if self._current:
            return self._current[0]
        return self

    async def exchange(self, c: Client) -> result.Ok | result.Error:
        async def image_transfer(tsk: task.ImageTransfer) -> result.Ok | result.Error:
            self.tasks.append(tsk)
            self._current.append(tsk)
            if isinstance((res_tr := await tsk.exchange(c)), result.Error):
                return res_tr
            self._current.remove(tsk)
            return result.OK

        firmwares: dict[tuple[tuple[int, int, int], str], bytes]
        boots: dict[tuple[int, str], bytes]
        res_boot_ver: result.SimpleOrError[cdt.CommonDataType]
        firmware_image_par = dlms_par.ImageTransfer.from_e()
        boot_image_par = dlms_par.ImageTransfer.from_e(128)
        if isinstance(res_firm_ver := await task.GetFirmwareVersion().exchange(c), result.Error):
            return res_firm_ver
        try:
            self.find_ver = SemVer.parse(
                version=bytes(res_firm_ver.value),
                optional_minor_and_patch=True
            )
            c.log(logL.INFO, F"find {self.find_ver}")
        except ValueError as e:    # todo: handle non semver type
            return result.Error.from_e(exc.DLMSException(), F"can't convert version to SemVer2.0: {e}")
        # select update algorithm by FirmwareVersion. Only for KPZ
        if self.find_ver >= SemVer(0, 0, 53):
            transfer_task = task.ImageTransfer
        elif self.find_ver >= SemVer(0, 0, 48):
            transfer_task = ImageTransferOld2
        elif self.find_ver >= SemVer(0, 0, 25):
            transfer_task = ImageTransferOld
        else:
            return result.Error.from_e(ValueError(), F"Невозможно обновить версию {self.find_ver}")
        if self.find_ver < SemVer(0, 0, 25):
            return result.Error.from_e(exc.VersionError(self.find_ver))
        if self.find_ver < SemVer(1, 4):
            if isinstance(res_firm_id := await task.Par2Data[cdt.CommonDataType](Parameter.parse("0.0.128.100.0.255:2")).exchange(c), result.Error):
                return res_firm_id.with_msg("firmware ID read")
            res_boot_ver = res_firm_id
        elif self.find_ver < SemVer(1, 8):
            if isinstance(res_firm_id := await task.Par2Data(dlms_par.ACTIVE_FIRMWARE_IDENTIFIER_0.value).exchange(c), result.Error):
                return res_firm_id.with_msg("firmware ID read")
            if isinstance(res_boot_ver := await task.Par2Data(Parameter.parse("0.0.128.100.0.255:2")).exchange(c), result.Error):
                return res_boot_ver.with_msg("boot Version read")
        else:
            return result.Error.from_e(exc.ITEApplication(), "Unknown metrology Version")
        # decide firm_id and boot_ver
        if (matching := firm_id_pat.search(bytes(res_firm_id.value))) is None:
            return result.Error.from_e(exc.ITEApplication(), F"not find Firmware ID in {res_firm_id.value}")
        firm_id: bytes = matching.group("fid")
        if (matching := boot_ver_pat.search(bytes(res_boot_ver.value))) is None:
            return result.Error.from_e(exc.ITEApplication(), F"not find boot ver in {res_firm_id.value}")
        boot_ver: int = int(matching.group("boot_ver"))
        # add optional object if its values absence
        suitable_firmware: SemVer = SemVer(0, 0, 1)
        suitable_boot: int = 0
        """ key of image for update """
        if not (firms := get_firmware(manufacturer := c.objects.id.man)):
            return result.Error.from_e(exc.ITEApplication(), F"not find firmwares for {manufacturer=}")
        firmwares, boots = firms
        # search boot image
        find_image: bytes = b""
        for (ver, desc), image in boots.items():
            if ver <= suitable_boot:
                continue
            if (
                (matching := firm_id_pat.search(bytes(desc, encoding="ascii"))) is not None
                and firm_id == matching.group("fid")
            ):
                suitable_boot = ver
                find_image = image
            else:
                """search more"""
        if (
            suitable_boot != boot_ver
            and find_image != b""
        ):
            c.log(logL.INFO, F"choice image to update {suitable_boot=}")
            if isinstance(res_transfer := await image_transfer(transfer_task(
                par=boot_image_par,
                image=find_image,
                msg=f"{suitable_boot}"
            )), result.Error):
                return res_transfer
        # search firmware image
        find_image = b""
        for (app_args, desc), image in firmwares.items():
            try:
                compare_ver = SemVer(*app_args)
            except ValueError as e:
                c.log(logL.ERR, F"Неизвестный тип {app_args} в *.dat файле: {e}")
                continue
            if compare_ver <= suitable_firmware:
                continue
            if (
                (matching := firm_id_pat.search(bytes(desc, encoding="ascii"))) is not None
                and firm_id == matching.group("fid")
            ):
                suitable_firmware = compare_ver
                find_image = image
            else:
                """search more"""
        if (
            suitable_firmware != self.find_ver
            and find_image != b""
        ):
            c.log(logL.INFO, F"choice image to update {suitable_firmware=}")
            if isinstance(res_transfer := await image_transfer(transfer_task(
                par=firmware_image_par,
                image=find_image,
                msg=f"{suitable_firmware}"
            )), result.Error):
                return res_transfer
            c._objects = None  # clear collection for pass LDN checked
            if isinstance(res_firm_ver := await task.GetFirmwareVersion().run(c), result.Error):  # to get new collection
                return res_firm_ver
        return result.OK
