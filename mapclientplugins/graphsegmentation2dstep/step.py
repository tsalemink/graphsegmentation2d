'''
MAP Client Plugin Step
'''
import json
from ast import literal_eval

from PySide2 import QtGui, QtWidgets

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.graphsegmentation2dstep.configuredialog import ConfigureDialog


class GraphSegmentation2DStep(WorkflowStepMountPoint):
    '''
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    '''

    def __init__(self, location):
        super(GraphSegmentation2DStep, self).__init__('Graph Segmentation 2D', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Segmentation'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/graphsegmentation2dstep/images/segmentation.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#plot_datasets'))
        # Port data:
        self._portData0 = None  # python#dict
        # Config:
        self._config = {}
        self._config['identifier'] = ''

    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        # Put your execute step code here before calling the '_doneExecution' method.
        markers = ['ko', 'kd', 'kh', 'k8', 'kv', 'k^', 'k<', 'k>']

        plot_datasets = dict()
        datasets = _extractDataSets(self._config)
        count = 1
        for dataset in datasets:
            plot_datasets['dataset_{0}'.format(count)] = {
                'label': dataset,
                'x': datasets[dataset][0::2],
                'y': datasets[dataset][1::2],
                'marker': markers[count % len(markers)],
            }
            count += 1

        self._portData0 = plot_datasets
        self._doneExecution()

    def getPortData(self, index):
        '''
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        '''
        return self._portData0  # python#dict

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog(self._main_window)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

    def serialize(self):
        '''
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        '''
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


def _extractDataSets(config):
    """
    Extract only the parameters from the configuration.

    :param config: dict of the complete configuration
    :return: dict of just the parameters.
    """
    parameters = {}
    for key in config:
        if key != 'identifier':
            values = config[key]
            parameters[values[0]] = values[1]

    return parameters
