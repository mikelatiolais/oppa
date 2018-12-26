"""OPPA Hardware interface.

Contains the hardware interface and drivers for the Open Pinball Project Arduino
platform hardware, including the solenoid, input, incandescent, and neopixel
boards.
"""
import logging
import asyncio
import serial

from mpf.platforms.interfaces.driver_platform_interface import PulseSettings, HoldSettings

from mpf.platforms.interfaces.switch_platform_interface import SwitchPlatformInterface

from mpf.core.platform import SwitchPlatform, DriverPlatform, LightsPlatform, SwitchSettings, DriverSettings, \
    DriverConfig, SwitchConfig

MYPY = False
if MYPY:   # pragma: no cover
    from typing import Dict, List, Set, Union


# pylint: disable-msg=too-many-instance-attributes
class OPPASwitch(SwitchPlatformInterface):

    """A switch in an OPPA setup."""

    def get_board_name(self):
        """Return name."""
        return "OPPA"

class OppaHardwarePlatform(LightsPlatform, SwitchPlatform, DriverPlatform):

    """Platform class for the OPPA hardware.

    Args:
        machine: The main ``MachineController`` instance.

    """

    __slots__ = ["opp_connection", "serial_connections", "opp_incands", "incandDict", "opp_solenoid", "solDict",
                 "opp_inputs", "inpDict", "inpAddrDict", "matrixInpAddrDict", "read_input_msg", "opp_neopixels",
                 "neoCardDict", "neoDict", "numGen2Brd", "gen2AddrArr", "badCRC", "minVersion", "_poll_task",
                 "config", "_poll_response_received", "machine_type", "opp_commands", "_incand_task"]

    def __init__(self, machine) -> None:
        """Initialise OPP platform."""
        super().__init__(machine)
        self.log = logging.getLogger('OPPA')
        self.log.info("Configuring OPPA hardware.")

        self.opp_connection = {}            # type: Dict[str, OPPSerialCommunicator]
        self._poll_task = {}                # type: Dict[str, asyncio.Task]
        self._incand_task = None            # type: asyncio.Task

        self.features['tickless'] = True
        self.inpDict = dict()               # type: Dict[str, OPPASwitch]



    @asyncio.coroutine
    def initialize(self):
        """Initialise connections to OPP hardware."""
        yield from self._connect_to_hardware()

    @asyncio.coroutine
    def start(self):
        """Start polling and listening for commands."""
        self._poll_task[serial] = self.machine.clock.loop.create_task(self._poll_oppa())

    def stop(self):
        """Stop hardware and close connections."""
        for task in self._poll_task.values():
            task.cancel()

        self._poll_task = {}

        for connections in self.serial_connections:
            connections.stop()

        self.serial_connections = []

    def __repr__(self):
        """Return string representation."""
        return '<Platform.OPPA>'

    def process_received_message(self, chain_serial, msg):
        """Send an incoming message from the OPP hardware to the proper method for servicing.

        Args:
            chain_serial: Serial of the chain which received the message.
            msg: Message to parse.
        """

    @staticmethod
    def _get_numbers(mask):
        number = 0
        ref = 1
        result = []
        while mask > ref:
            if mask & ref:
                result.append(number)
            number += 1
            ref = ref << 1

        return result

    def get_info_string(self):
        """Dump infos about boards."""
        if not self.serial_connections:
            return "No connection to any CPU board."


        infos += "\nInput cards:\n"

        return infos

    @asyncio.coroutine
    def _connect_to_hardware(self):
        """Connect to each port from the config.

        This process will cause the OPPSerialCommunicator to figure out which chains they've connected to
        and to register themselves.
        """
        # self.opp_connection = serial.Serial(self.config['device'], self.config['baud']);
        self.opp_connection = serial.Serial('/dev/ttyACM0', 115200);
        

    def update_incand(self):
        """Update all the incandescents connected to OPP hardware.

        This is done once per game loop if changes have been made.

        It is currently assumed that the UART oversampling will guarantee proper
        communication with the boards.  If this does not end up being the case,
        this will be changed to update all the incandescents each loop.
        """

    @classmethod
    def get_coil_config_section(cls):
        """Return coil config section."""
        return "opp_coils"

    @asyncio.coroutine
    def get_hw_switch_states(self):
        """Get initial hardware switch states.

        This changes switches from active low to active high
        """
        hw_states = dict()
        hw_states[str(0)] = 0

        return hw_states

    def inv_resp(self, chain_serial, msg):
        """Parse inventory response.

        Args:
            chain_serial: Serial of the chain which received the message.
            msg: Message to parse.
        """

    @staticmethod
    def eom_resp(chain_serial, msg):
        """Process an EOM.

        Args:
            chain_serial: Serial of the chain which received the message.
            msg: Message to parse.
        """
        # An EOM command can be used to resynchronize communications if message synch is lost
        pass

    def get_gen2_cfg_resp(self, chain_serial, msg):
        """Process cfg response.

        Args:
            chain_serial: Serial of the chain which received the message.
            msg: Message to parse.
        """
        # Multiple get gen2 cfg responses can be received at once

    def vers_resp(self, chain_serial, msg):
        """Process version response.

        Args:
            chain_serial: Serial of the chain which received the message.
            msg: Message to parse.
        """
        # Multiple get version responses can be received at once

    def read_gen2_inp_resp_initial(self, chain_serial, msg):
        """Read initial switch states.

        Args:
            chain_serial: Serial of the chain which received the message.
            msg: Message to parse.
        """

    def read_gen2_inp_resp(self, chain_serial, msg):
        """Read switch changes.

        Args:
            chain_serial: Serial of the chain which received the message.
            msg: Message to parse.
        """

    def read_matrix_inp_resp_initial(self, chain_serial, msg):
        """Read initial matrix switch states.

        Args:
            chain_serial: Serial of the chain which received the message.
            msg: Message to parse.
        """

    # pylint: disable-msg=too-many-nested-blocks
    def read_matrix_inp_resp(self, chain_serial, msg):
        """Read matrix switch changes.

        Args:
            chain_serial: Serial of the chain which received the message.
            msg: Message to parse.
        """

    def _get_dict_index(self, input_str):
        return input_str

    def configure_driver(self, config: DriverConfig, number: str, platform_settings: dict):
        """Configure a driver.

        Args:
            config: Config dict.
        """
        if not self.opp_connection:
            raise AssertionError("A request was made to configure an OPP solenoid, "
                                 "but no OPP connection is available")

        number = self._get_dict_index(number)

        if number not in self.solDict:
            raise AssertionError("A request was made to configure an OPP solenoid "
                                 "with number {} which doesn't exist".format(number))

        # Use new update individual solenoid command
        opp_sol = self.solDict[number]
        opp_sol.config = config
        opp_sol.platform_settings = platform_settings
        self.log.debug("Configure driver %s", number)
        default_pulse = PulseSettings(config.default_pulse_power, config.default_pulse_ms)
        default_hold = HoldSettings(config.default_hold_power)
        opp_sol.reconfigure_driver(default_pulse, default_hold)

        # Removing the default input is not necessary since the
        # CFG_SOL_USE_SWITCH is not being set

        return opp_sol

    def configure_switch(self, number: str, config: SwitchConfig, platform_config: dict):
        """Configure a switch.

        Args:
            config: Config dict.
        """
        return OPPASwitch(config, number)

    def parse_light_number_to_channels(self, number: str, subtype: str):
        """Parse number and subtype to channel."""
        if subtype == "matrix":
            return [
                {
                    "number": self._get_dict_index(number)
                }
            ]
        elif not subtype or subtype == "led":
            return [
                {
                    "number": self._get_dict_index(number) + "-0"
                },
                {
                    "number": self._get_dict_index(number) + "-1"
                },
                {
                    "number": self._get_dict_index(number) + "-2"
                },
            ]
        else:
            raise AssertionError("Unknown subtype {}".format(subtype))

    def configure_light(self, number, subtype, platform_settings):
        """Configure a led or matrix light."""
        if not self.opp_connection:
            raise AssertionError("A request was made to configure an OPP light, "
                                 "but no OPP connection is available")
        if not subtype or subtype == "led":
            chain_serial, card, pixel_num, index_str = number.split('-')
            index = chain_serial + '-' + card
            if index not in self.neoCardDict:
                raise AssertionError("A request was made to configure an OPP neopixel "
                                     "with card number {} which doesn't exist".format(card))

            neo = self.neoCardDict[index]
            channel = neo.add_channel(int(pixel_num), self.neoDict, index_str)
            return channel
        elif subtype == "matrix":
            if number not in self.incandDict:
                raise AssertionError("A request was made to configure a OPP matrix "
                                     "light (incand board), with number {} "
                                     "which doesn't exist".format(number))

            return self.incandDict[number]
        else:
            raise AssertionError("Unknown subtype {}".format(subtype))

    def light_sync(self):
        """Update lights.

        Currently we only update neo pixels. Incands are updated separately in a task to provide better batching.
        """
        for light in self.neoDict.values():
            if light.dirty:
                light.update_color()

    @staticmethod
    def _done(future):  # pragma: no cover
        """Evaluate result of task.

        Will raise exceptions from within task.
        """
        future.result()

    @asyncio.coroutine
    def _poll_oppa(self):
        """Poll switches."""
        while True:
            # wait for previous poll response
            timeout = 1 / self.config['poll_hz'] * 25
            try:
                yield from asyncio.wait_for(self._poll_response_received[chain_serial].wait(), timeout,
                                            loop=self.machine.clock.loop)
            except asyncio.TimeoutError:
                self.log.warning("Poll took more than %sms for %s", timeout * 1000, chain_serial)
            else:
                self._poll_response_received[chain_serial].clear()
            # send poll
            self.send_to_processor(chain_serial, self.read_input_msg[chain_serial])
            yield from self.opp_connection[chain_serial].writer.drain()
            # the line above saturates the link and seems to overwhelm the hardware. limit it to 100Hz
            yield from asyncio.sleep(1 / self.config['poll_hz'], loop=self.machine.clock.loop)

    def _verify_coil_and_switch_fit(self, switch, coil):
        chain_serial, card, solenoid = coil.hw_driver.number.split('-')
        sw_chain_serial, sw_card, sw_num = switch.hw_switch.number.split('-')
        if self.minVersion >= 0x00020000:
            if chain_serial != sw_chain_serial or card != sw_card:
                raise AssertionError('Invalid switch being configured for driver. Driver = %s '
                                     'Switch = %s. For Firmware 0.2.0+ driver and switch have to be on the same board.'
                                     % (coil.hw_driver.number, switch.hw_switch.number))
        else:
            matching_sw = ((int(solenoid) & 0x0c) << 1) | (int(solenoid) & 0x03)
            if chain_serial != sw_chain_serial or card != sw_card or matching_sw != int(sw_num):
                raise AssertionError('Invalid switch being configured for driver. Driver = %s '
                                     'Switch = %s. For Firmware < 0.2.0 they have to be on the same board and have the '
                                     'same number' % (coil.hw_driver.number, switch.hw_switch.number))

    def set_pulse_on_hit_rule(self, enable_switch: SwitchSettings, coil: DriverSettings):
        """Set pulse on hit rule on driver.

        Pulses a driver when a switch is hit. When the switch is released the pulse continues. Typically used for
        autofire coils such as pop bumpers.
        """
        self._write_hw_rule(enable_switch, coil, use_hold=False, can_cancel=False)

    def set_pulse_on_hit_and_release_rule(self, enable_switch: SwitchSettings, coil: DriverSettings):
        """Set pulse on hit and release rule to driver.

        Pulses a driver when a switch is hit. When the switch is released the pulse is canceled. Typically used on
        the main coil for dual coil flippers without eos switch.
        """
        self._write_hw_rule(enable_switch, coil, use_hold=False, can_cancel=True)

    def set_pulse_on_hit_and_enable_and_release_rule(self, enable_switch: SwitchSettings, coil: DriverSettings):
        """Set pulse on hit and enable and relase rule on driver.

        Pulses a driver when a switch is hit. Then enables the driver (may be with pwm). When the switch is released
        the pulse is canceled and the driver gets disabled. Typically used for single coil flippers.
        """
        self._write_hw_rule(enable_switch, coil, use_hold=True, can_cancel=True)

    def set_pulse_on_hit_and_enable_and_release_and_disable_rule(self, enable_switch: SwitchSettings,
                                                                 disable_switch: SwitchSettings, coil: DriverSettings):
        """Set pulse on hit and enable and release and disable rule on driver.

        Pulses a driver when a switch is hit. Then enables the driver (may be with pwm). When the switch is released
        the pulse is canceled and the driver gets disabled. When the second disable_switch is hit the pulse is canceled
        and the driver gets disabled. Typically used on the main coil for dual coil flippers with eos switch.
        """
        raise AssertionError("Not implemented in OPP currently")

    def _write_hw_rule(self, switch_obj: SwitchSettings, driver_obj: DriverSettings, use_hold, can_cancel=False):
        if switch_obj.invert:
            raise AssertionError("Cannot handle inverted switches")

        if driver_obj.hold_settings and not use_hold:
            raise AssertionError("Invalid call")

        self._verify_coil_and_switch_fit(switch_obj, driver_obj)

        self.log.debug("Setting HW Rule. Driver: %s", driver_obj.hw_driver.number)

        driver_obj.hw_driver.switches.append(switch_obj.hw_switch.number)
        driver_obj.hw_driver.set_switch_rule(driver_obj.pulse_settings, driver_obj.hold_settings, driver_obj.recycle,
                                             can_cancel)
        _, _, switch_num = switch_obj.hw_switch.number.split("-")
        switch_num = int(switch_num)
        self._add_switch_coil_mapping(switch_num, driver_obj.hw_driver)

    def _remove_switch_coil_mapping(self, switch_num, driver):
        """Remove mapping between switch and coil."""
        if self.minVersion < 0x00020000:
            return

        _, _, coil_num = driver.number.split('-')
        msg = bytearray()
        msg.append(driver.solCard.addr)
        msg.extend(OppRs232Intf.SET_SOL_INP_CMD)
        msg.append(int(switch_num))
        msg.append(int(coil_num) + ord(OppRs232Intf.CFG_SOL_INP_REMOVE))
        msg.extend(OppRs232Intf.calc_crc8_whole_msg(msg))
        msg.extend(OppRs232Intf.EOM_CMD)
        final_cmd = bytes(msg)

        self.log.debug("Unmapping input %s and coil %s", switch_num, coil_num)
        self.send_to_processor(driver.solCard.chain_serial, final_cmd)

    def _add_switch_coil_mapping(self, switch_num, driver):
        """Add mapping between switch and coil."""
        if self.minVersion < 0x00020000:
            return
        _, _, coil_num = driver.number.split('-')
        msg = bytearray()
        msg.append(driver.solCard.addr)
        msg.extend(OppRs232Intf.SET_SOL_INP_CMD)
        msg.append(int(switch_num))
        msg.append(int(coil_num))
        msg.extend(OppRs232Intf.calc_crc8_whole_msg(msg))
        msg.extend(OppRs232Intf.EOM_CMD)
        final_cmd = bytes(msg)

        self.log.debug("Mapping input %s and coil %s", switch_num, coil_num)
        self.send_to_processor(driver.solCard.chain_serial, final_cmd)

    def clear_hw_rule(self, switch: SwitchSettings, coil: DriverSettings):
        """Clear a hardware rule.

        This is used if you want to remove the linkage between a switch and
        some driver activity. For example, if you wanted to disable your
        flippers (so that a player pushing the flipper buttons wouldn't cause
        the flippers to flip), you'd call this method with your flipper button
        as the *sw_num*.

        """
        if switch.hw_switch.number in coil.hw_driver.switches:
            self.log.debug("Clearing HW Rule for switch: %s, coils: %s", switch.hw_switch.number,
                           coil.hw_driver.number)
            coil.hw_driver.switches.remove(switch.hw_switch.number)
            _, _, switch_num = switch.hw_switch.number.split("-")
            switch_num = int(switch_num)
            self._remove_switch_coil_mapping(switch_num, coil.hw_driver)

        # disable rule if there are no more switches
        # Technically not necessary unless the solenoid parameters are
        # changing.  MPF may not know when initial kick and hold values
        # are changed, so this might need to be called each time.
        if not coil.hw_driver.switches:
            coil.hw_driver.remove_switch_rule()


