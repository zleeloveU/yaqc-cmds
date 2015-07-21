### import ####################################################################

import time

import numpy as np

from PyQt4 import QtCore

import project_globals as g

import WrightTools.units as wt_units


### gui items #################################################################


class Value(QtCore.QMutex):

    def __init__(self, initial_value=None):
        '''
        basic QMutex object to hold a single object in a thread-safe way
        '''
        QtCore.QMutex.__init__(self)
        self.value = initial_value

    def read(self):
        return self.value

    def write(self, value):
        '''
        bool value
        '''
        self.lock()
        self.value = value
        self.unlock()


class PyCMDS_Object(QtCore.QObject):
    updated = QtCore.pyqtSignal()
    disabled = False

    def __init__(self, initial_value=None,
                 ini=None, section='', option='',
                 import_from_ini=False, save_to_ini_at_shutdown=False,
                 display=False, name='', label = '', set_method=None):
        QtCore.QObject.__init__(self)
        self.has_widget = False
        self.tool_tip = ''
        self.value = Value(initial_value)
        self.display = display
        self.set_method = set_method
        if self.display:
            self.disabled = True
        else:
            self.disabled = False
        # ini
        if ini:
            self.has_ini = True
            self.ini = ini
            self.section = section
            self.option = option
        else:
            self.has_ini = False
        if import_from_ini:
            self.get_saved()
        if save_to_ini_at_shutdown:
            g.shutdown.add_method(self.save)
        # name
        self.name = name
        if not label == '':
            pass
        else:
            self.label = self.name

    def read(self):
        return self.value.read()

    def write(self, value):
        self.value.write(value)
        self.updated.emit()

    def get_saved(self):
        if self.has_ini:
            self.value.write(self.ini.read(self.section, self.option))
        self.updated.emit()
        return self.value.read()
        
    def save(self, value=None):
        if value is not None:
            self.value.write(value)
        if self.has_ini:
            self.ini.write(self.section, self.option, self.value.read())

    def set_disabled(self, disabled):
        self.disabled = disabled
        if self.has_widget:
            self.widget.setDisabled(self.disabled)

    def set_tool_tip(self, tool_tip):
        self.tool_tip = tool_tip
        if self.has_widget:
            self.widget.setToolTip(self.tool_tip)


class Bool(PyCMDS_Object):
    '''
    holds 'value' (bool) - the state of the checkbox
    
    use read method to access
    '''
    
    def __init__(self, initial_value = False, 
                 ini = None, section='', option='', display=False, name='',
                 import_from_ini = False, save_to_ini_at_shutdown = False):
        PyCMDS_Object.__init__(self, initial_value=initial_value,
                               ini=ini, section=section, option=option,
                               import_from_ini=import_from_ini,
                               save_to_ini_at_shutdown=save_to_ini_at_shutdown,
                               display=display, name=name)
        self.type = 'checkbox'
    def give_control(self, control_widget):
        self.widget = control_widget
        #set
        self.widget.setChecked(self.value.read())   
        #connect signals and slots
        self.updated.connect(lambda: self.widget.setChecked(self.value.read()))
        self.widget.stateChanged.connect(lambda: self.write(self.widget.checkState()))
        #finish
        self.widget.setToolTip(self.tool_tip)
        self.widget.setDisabled(self.disabled)
        self.has_widget = True


class Combo(PyCMDS_Object):

    def __init__(self, allowed_values, initial_value=None, 
                 ini=None, section=None, option=None, import_from_ini = False, 
                 save_to_ini_at_shutdown = False, display=False, name='',
                 set_method=None):
        PyCMDS_Object.__init__(self, initial_value=initial_value,
                               ini=ini, section=section, option=option,
                               import_from_ini=import_from_ini,
                               save_to_ini_at_shutdown=save_to_ini_at_shutdown,
                               display=display, name=name, 
                               set_method=set_method)
        self.type = 'combo'
        self.allowed_values = allowed_values
        self.data_type = type(allowed_values[0])

    def associate(self, display=None, pre_name=''):
        # display
        if display is None:
            display = self.display
        # name
        name = pre_name + self.name
        # new object
        new_obj = Combo(initial_value=self.read(), display=display,
                        allowed_values=self.allowed_values, name=name)
        return new_obj

    def save(self, value=None):
        if value is not None:
            self.value.write(value)
        if self.has_ini:
            self.ini.write(self.section, self.option, self.value.read(), with_apostrophe=True)

    def write(self, value):
        # value will be maintained as original data type
        value = self.data_type(value)
        PyCMDS_Object.write(self, value)

    def give_control(self, control_widget):
        self.widget = control_widget
        # fill out items
        allowed_values_strings = [str(value) for value in self.allowed_values]
        self.widget.addItems(allowed_values_strings)
        self.widget.setCurrentIndex(allowed_values_strings.index(str(self.read())))       
        # connect signals and slots
        self.updated.connect(lambda: self.widget.setCurrentIndex(allowed_values_strings.index(str(self.read()))))
        self.widget.currentIndexChanged.connect(lambda: self.write(self.widget.currentText()))
        self.widget.setToolTip(self.tool_tip)
        self.widget.setDisabled(self.disabled)
        self.has_widget = True


class Filepath(PyCMDS_Object):
    '''
    holds 'value' (str) - the filepath as a string
    '''
    def __init__(self, initial_value = None, ini = None, import_from_ini = False, save_to_ini_at_shutdown = False):
        gui_object.__init__(self, initial_value = initial_value, ini_inputs = ini, import_from_ini = import_from_ini, save_to_ini_at_shutdown = save_to_ini_at_shutdown)
        self.type = 'filepath'
    def give_control(self, control_widget):
        self.widget = control_widget
        '''
        #fill out items
        self.widget.addItems(self.allowed_values)
        self.widget.setCurrentIndex(self.allowed_values.index(self.read()))       
        #connect signals and slots
        self.updated.connect(lambda: self.widget.setCurrentIndex(self.allowed_values.index(self.read())))
        self.widget.currentIndexChanged.connect(lambda: self.write(self.widget.currentText()))
        '''
        self.widget.setToolTip(self.tool_tip)
        self.widget.setDisabled(self.disabled)
        self.has_widget = True
    def give_button(self, button_widget):
        self.button = button_widget


class NumberLimits(PyCMDS_Object):

    def __init__(self, min_value=-1000000., max_value=1000000., units=None):
        '''
        not appropriate for use as a gui element - only for backend use
        units must never change for this kind of object
        '''
        PyCMDS_Object.__init__(self)
        PyCMDS_Object.write(self, [min_value, max_value])
        self.units = units

    def read(self, output_units='same'):
        min_value, max_value = PyCMDS_Object.read(self)
        if output_units == 'same':
            pass
        else:
            min_value = wt_units.converter(min_value, self.units, output_units)
            max_value = wt_units.converter(max_value, self.units, output_units)
        # ensure order
        min_value, max_value = [min([min_value, max_value]),
                                max([min_value, max_value])]
        return [min_value, max_value]

    def write(self, min_value, max_value, input_units='same'):
        if input_units == 'same':
            pass
        else:
            min_value = wt_units.converter(min_value, input_units, self.units)
            max_value = wt_units.converter(max_value, input_units, self.units)
        # ensure order
        min_value, max_value = [min([min_value, max_value]),
                                max([min_value, max_value])]
        PyCMDS_Object.write(self, [min_value, max_value])
        self.updated.emit()


class Number(PyCMDS_Object):
    
    def __init__(self, initial_value=np.nan, display=False, name='',
                 ini=None, section='', option='',
                 import_from_ini=False, save_to_ini_at_shutdown=False,
                 units=None, limits=NumberLimits(),
                 single_step=1., decimals=2, set_method=None):
        PyCMDS_Object.__init__(self, initial_value=initial_value,
                               ini=ini, section=section, option=option,
                               import_from_ini=import_from_ini,
                               save_to_ini_at_shutdown=save_to_ini_at_shutdown,
                               display=display, name=name, 
                               set_method=set_method)
        self.type = 'number'
        self.single_step = single_step
        self.decimals = decimals
        self.set_control_steps(single_step, decimals)
        # units
        self.units = units
        self.units_kind = None
        for dic in wt_units.unit_dicts:
            if self.units in dic.keys():
                self.units_dic = dic
                self.units_kind = dic['kind']
        # limits
        self.limits = limits
        self._set_limits()
        self.limits.updated.connect(lambda: self._set_limits())

    def associate(self, display=None, pre_name=''):
        # display
        if display is None:
            display = self.display
        # name
        name = pre_name + self.name
        # new object
        new_obj = Number(initial_value=self.read(), display=display,
                         units=self.units, limits=self.limits,
                         single_step=self.single_step,
                         decimals=self.decimals, name=name)
        return new_obj

    def convert(self, destination_units):
        # value
        old_val = self.value.read()
        new_val = wt_units.converter(old_val, self.units, str(destination_units))
        self.value.write(new_val)
        # commit and signal
        self.units = str(destination_units)
        self._set_limits()
        self.updated.emit()

    def read(self, output_units='same'):
        value = PyCMDS_Object.read(self)
        if output_units == 'same':
            pass
        else:
            value = wt_units.converter(value, self.units, output_units)
        return value

    def set_control_steps(self, single_step=None, decimals=None):
        limits = [self.single_step, self.decimals]
        inputs = [single_step, decimals]
        widget_methods = ['setSingleStep', 'setDecimals']
        for i in range(len(limits)):
                if not inputs[i] is None:
                    limits[i] = inputs[i]
                if self.has_widget:
                    getattr(self.widget, widget_methods[i])(limits[i])

    def give_control(self, control_widget):
        self.widget = control_widget
        # set values
        #self.widget.setMinimum(self.min_value.read())
        #self.widget.setMaximum(self.max_value.read())
        self.widget.setDecimals(self.decimals)
        self.widget.setSingleStep(self.single_step)
        self.widget.setValue(self.value.read())
        # connect signals and slots
        self.updated.connect(lambda: self.widget.setValue(self.value.read()))
        self.widget.editingFinished.connect(lambda: self.write(self.widget.value()))
        # finish
        self.widget.setToolTip(self.tool_tip)
        self.has_widget = True
        self._set_limits()
        
    def give_units_combo(self, units_combo_widget):
        self.units_widget = units_combo_widget
        # add items
        unit_types = self.units_dic.keys()
        unit_types.remove('kind')
        self.units_widget.addItems(unit_types)
        # set current item
        self.units_widget.setCurrentIndex(unit_types.index(self.units))
        # associate update with conversion 
        self.units_widget.currentIndexChanged.connect(lambda: self.convert(self.units_widget.currentText()))

    def write(self, value, input_units='same'):
        if input_units == 'same':
            pass
        else:
            value = wt_units.converter(value, input_units, self.units)
        PyCMDS_Object.write(self, value)

    def _set_limits(self):
        min_value, max_value = self.limits.read()
        limits_units = self.limits.units
        min_value = wt_units.converter(min_value, limits_units, self.units)
        max_value = wt_units.converter(max_value, limits_units, self.units)
        # ensure order
        min_value, max_value = [min([min_value, max_value]),
                                max([min_value, max_value])]
        if self.has_widget:
            self.widget.setMinimum(min_value)
            self.widget.setMaximum(max_value)
        if not self.display:
            self.set_tool_tip('min: ' + str(min_value) + '\n' +
                              'max: ' + str(max_value))


class String(PyCMDS_Object):
    '''
    holds 'value' (string)
    '''
    def __init__(self, initial_value = None, ini = None, import_from_ini = False, save_to_ini_at_shutdown = False):
        gui_object.__init__(self, initial_value = initial_value, ini_inputs = ini, import_from_ini = import_from_ini, save_to_ini_at_shutdown = save_to_ini_at_shutdown)
    def give_control(self, control_widget):
        self.widget = control_widget
        #fill out items
        self.widget.setText(self.value)       
        #connect signals and slots
        self.updated.connect(lambda: self.widget.setText(self.value))
        self.widget.editingFinished.connect(lambda: self.write(self.widget.text()))
        self.widget.setToolTip(self.tool_tip)
        self.has_widget = True    

    
### hardware ##################################################################


class Busy(QtCore.QMutex):

    def __init__(self):
        '''
        QMutex object to communicate between threads that need to wait \n
        while busy.read(): busy.wait_for_update()
        '''
        QtCore.QMutex.__init__(self)
        self.WaitCondition = QtCore.QWaitCondition()
        self.value = False
        self.type = 'busy'
        self.update_signal = None

    def read(self):
        return self.value

    def write(self, value):
        '''
        bool value
        '''
        self.lock()
        self.value = value
        self.WaitCondition.wakeAll()
        self.unlock()

    def wait_for_update(self, timeout=5000):
        '''
        wait in calling thread for any thread to call 'write' method \n
        int timeout in milliseconds
        '''
        if self.value:
            return self.WaitCondition.wait(self, msecs=timeout)


class Address(QtCore.QObject):
    update_ui = QtCore.pyqtSignal()
    queue_emptied = QtCore.pyqtSignal()
    
    def __init__(self, enqueued_obj, busy_obj, name, ctrl_class):
        '''
        do not override __init__ or dequeue
        unless you really know what you are doing
        '''
        QtCore.QObject.__init__(self)
        self.enqueued = enqueued_obj
        self.busy = busy_obj
        self.name = name
        self.ctrl = ctrl_class(self.check_busy)
        self.exposed = self.ctrl.exposed
        for obj in self.exposed:
            if hasattr(self, obj.set_method):
                pass  # don't allow overwriting of address methods
            else:
                additional_method = getattr(self.ctrl, obj.set_method)
                setattr(self, obj.set_method, additional_method)
        self.gui = self.ctrl.gui
        self.native_units = self.ctrl.native_units
        self.limits = self.ctrl.limits
  
    @QtCore.pyqtSlot(str, list)
    def dequeue(self, method, inputs):
        '''
        accepts queued signals from 'queue' (address using q method) \n
        string method, list inputs
        '''
        self.update_ui.emit()
        if g.debug.read():
            print self.name, 'dequeue:', method, inputs
        # execute method
        getattr(self, str(method))(inputs)  # method passed as qstring
        # remove method from enqueued
        self.enqueued.pop()
        if not self.enqueued.read():
            self.queue_emptied.emit()
            self.check_busy([])
            self.update_ui.emit()

    def check_busy(self, inputs):
        '''
        decides if the hardware is done and handles writing of 'busy' to False
        '''
        # must always write busy whether answer is True or False
        if self.ctrl.is_busy():
            time.sleep(0.01)  # don't loop like crazy
            self.busy.write(True)
        elif self.enqueued.read():
            time.sleep(0.1)  # don't loop like crazy
            self.busy.write(True)
        else:
            self.busy.write(False)
            self.update_ui.emit()

    def get_position(self, inputs):
        self.ctrl.get_position()
        self.update_ui.emit()

    def poll(self, inputs):
        '''
        polling only gets enqueued by Hardware when not in module control
        '''
        self.get_position([])
        self.is_busy([])

    def initialize(self, inputs):
        self.ctrl.initialize(inputs)
        g.logger.log('info', self.name + ' Initializing', message=str(inputs))
        if g.debug.read():
            print self.name, 'initialization complete'

    def set_position(self, inputs):
        self.ctrl.set_position(inputs[0])
        self.get_position([])

    def close(self, inputs):
        self.ctrl.close()


class Enqueued(QtCore.QMutex):

    def __init__(self):
        '''
        holds list of enqueued options
        '''
        QtCore.QMutex.__init__(self)
        self.value = []

    def read(self):
        return self.value

    def push(self, value):
        self.lock()
        self.value.append(value)
        self.unlock()

    def pop(self):
        self.lock()
        self.value = self.value[1:]
        self.unlock()


class Q:

    def __init__(self, enqueued, busy, address):
        self.enqueued = enqueued
        self.busy = busy
        self.address = address
        self.queue = QtCore.QMetaObject()

    def push(self, method, inputs=[]):
        self.enqueued.push([method, time.time()])
        self.busy.write(True)
        # send Qt SIGNAL to address thread
        self.queue.invokeMethod(self.address,
                                'dequeue',
                                QtCore.Qt.QueuedConnection,
                                QtCore.Q_ARG(str, method),
                                QtCore.Q_ARG(list, inputs))


class Hardware(QtCore.QObject):
    update_ui = QtCore.pyqtSignal()

    def __init__(self, control_class, control_arguments, address_class=Address,
                 name='', initialize_hardware=True):
        '''
        container for all objects relating to a single piece
        of addressable hardware
        '''
        QtCore.QObject.__init__(self)
        self.name = name
        # create objects
        self.thread = QtCore.QThread()
        self.enqueued = Enqueued()
        self.busy = Busy()
        self.address = address_class(self.enqueued, self.busy,
                                     name, control_class)
        self.exposed = self.address.exposed
        self.current_position = self.exposed[0]
        self.gui = self.address.gui
        self.native_units = self.address.native_units
        self.limits = self.address.limits
        self.q = Q(self.enqueued, self.busy, self.address)
        # start thread
        self.address.moveToThread(self.thread)
        self.thread.start()
        # connect to address object signals
        self.address.update_ui.connect(self.update)
        for obj in self.exposed:
            obj.updated.connect(self.update)
        self.busy.update_signal = self.address.update_ui
        # initialize hardware
        self.q.push('initialize', control_arguments)
        # integrate close into PyCMDS shutdown
        self.shutdown_timeout = 30  # seconds
        g.shutdown.add_method(self.close)
        g.hardware_waits.add(self.wait_until_still)

    def close(self):
        # begin hardware shutdown
        self.q.push('close')
        # wait for hardware shutdown to complete
        start_time = time.time()
        while self.busy.read():
            if time.time()-start_time < self.shutdown_timeout:
                if not self.enqueued.read():
                    self.q.push('check_busy')
                self.busy.wait_for_update()
            else:
                g.logger.log('warning',
                             'Wait until done timed out',
                             self.name)
                break
        # quit thread
        self.thread.exit()
        self.thread.quit()

    def get_position(self):
        return self.current_position.read()

    def is_valid(self, destination, input_units=None):
        if input_units is None:
            pass
        else:
            destination = wt_units.converter(destination,
                                             input_units,
                                             self.native_units)
        min_value, max_value = self.limits.read(self.native_units)
        if min_value <= destination <= max_value:
            return True
        else:
            return False

    def poll(self, force=False):
        if force:
            self.q.push('poll')
            self.get_position()
        elif not g.module_control.read():
            self.q.push('poll')
            self.get_position()

    def set_position(self, destination, input_units=None):
        # must launch comove
        #   sent - destination
        #   recieved - busy object to be waited on once
        if input_units is None:
            pass
        else:
            destination = wt_units.converter(destination, 
                                             input_units, 
                                             self.native_units)
        self.q.push('set_position', [destination])

    def update(self):
        self.update_ui.emit()

    def wait_until_still(self):
        while self.busy.read():
            self.busy.wait_for_update()