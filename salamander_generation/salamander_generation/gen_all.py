""" Generate package """

import os
from collections import OrderedDict

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

from .gen_controller import ControlParameters
from.yaml_utils import ordered_dump


def create_directory(folder):
    """ Create directory if it does not exist """
    directory = os.path.dirname(folder)
    if not os.path.exists(directory):
        print("{} does not exist, creating directory".format(directory))
        os.makedirs(directory)


def generate_plugins(config_package, folder_path, home):
    """ Generate plugins configs """
    for plugin in config_package.model.plugins:
        if plugin.filename:
            dest = "{}config/{}".format(
                folder_path,
                plugin.filename
            )
            if "filename" in plugin.config:
                plugin.config["filename"] = (
                    folder_path
                    + plugin.config["filename"]
                )
                create_directory(home+plugin.config["filename"])
            create_directory(home+dest)
            with open(home+dest, "w+") as plugin_config:
                plugin_config.write(ordered_dump(plugin.config))


class ModelGenerationTemplates:
    """ Diagram templates """

    def __init__(self):
        super(ModelGenerationTemplates, self).__init__()
        self.env = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "templates")
        ))
        self.sdf = self.env.get_template('salamander.sdf')
        self.parameter = self.env.get_template('parameters.xml')
        self.model = self.env.get_template('model.config')
        self.plugin = self.env.get_template('plugin.xml')
        self.world = self.env.get_template('world.world')

    def render(self, config_package):
        """ Render Model """
        model_name = config_package.model.name
        folder_path = "/{}{}/".format(
            config_package.path,
            model_name
        )
        home = os.path.expanduser("~")
        create_directory(home+folder_path)
        # Get environment and templates
        filename_sdf = "model.sdf"
        filename_model = "model.config"
        filename_world = "world.world"
        # parameters = self.get_parameters(config_control)
        _plugins = "\n".join([
            self.plugin.render(
                plugin_filename=plugin.library,
                plugin_name=plugin.name,
                parameters="<config>{}config/{}</config>".format(
                    folder_path,
                    plugin.filename
                )
            )
            for plugin in config_package.model.plugins
        ])
        # Generate sdf
        self.generate_sdf(
            filename_sdf,
            config_package,
            _plugins,
            home+folder_path
        )
        # Generate model config
        self.generate_model_config(
            model_name=model_name,
            filename_sdf=filename_sdf,
            filename_model=filename_model,
            config_package=config_package,
            path=home+folder_path
        )
        # Generate plugins configs
        generate_plugins(
            config_package,
            folder_path,
            home
        )
        # Generate world
        self.generate_world(
            config_package,
            home+folder_path,
            filename_world
        )

    def generate_sdf(self, filename, config_package, plugins, path):
        """ Generate SDF """
        sdf = self.sdf.render(
            name=config_package.model.name,
            plugins=plugins,
            base_model=config_package.model.base_model
        )
        with open(path+filename, "w+") as fileobject:
            fileobject.write(sdf)
            print("  Generation of {} sdf complete".format(filename))

    def generate_model_config(self, config_package, path, **kwargs):
        """ Generate model config """
        model_name = kwargs.pop("model", "salamander_default_name")
        filename_sdf = kwargs.pop("filename_sdf", "model.sdf")
        filename_model = kwargs.pop("filename_model", "model.config")
        model = self.model.render(
            model_name=model_name,
            filename_sdf=filename_sdf,
            version=config_package.model.version,
            author=config_package.creator.name,
            email=config_package.creator.email
        )
        with open(path+filename_model, "w+") as fileobject:
            fileobject.write(model)
            print("  Generation of {} model complete".format(filename_model))

    def generate_world(self, config_package, path, filename_world):
        """ Generate world """
        world = self.world.render(
            name="salamander",
            uri="model://{}".format(config_package.model.name),
            pose="0 0 0 0 0 0"
        )
        with open(path+filename_world, "w+") as fileobject:
            fileobject.write(world)
            print("  Generation of {} sdf complete".format(filename_world))

    def get_parameters(self, config):
        """ Get parameters """
        parameters = []
        for _name in config:
            self.get_parameter(parameters, _name, config[_name])
        return parameters

    def get_parameter(self, parameters, name, value, **kwargs):
        """ Get parameter """
        prefix = kwargs.pop("prefix", "")
        sep = kwargs.pop("sep", "_")
        if isinstance(value, (dict, OrderedDict)):
            for _name in value:
                self.get_parameter(
                    parameters,
                    _name,
                    value[_name],
                    prefix=prefix+name+sep,
                    sep=sep
                )
        else:
            parameters.append(
                self.parameter.render(
                    parameter_name=prefix+name,
                    parameter_value=value
                )
            )
        return parameters


class Creator(OrderedDict):
    """ Creator """

    def __init__(self, name, email):
        super(Creator, self).__init__()
        self["name"] = name
        self["email"] = email

    @property
    def name(self):
        """ Name """
        return self["name"]

    @property
    def email(self):
        """ Email """
        return self["email"]


class Model(OrderedDict):
    """ Model """

    def __init__(self, name, base_model, plugins, version):
        super(Model, self).__init__()
        self["name"] = name
        self["base_model"] = base_model
        self["plugins"] = plugins
        self["version"] = version

    @property
    def name(self):
        """ Name """
        return self["name"]

    @property
    def base_model(self):
        """ Base model """
        return self["base_model"]

    @property
    def plugins(self):
        """ Plugins """
        return self["plugins"]

    @property
    def version(self):
        """ Version """
        return self["version"]


class Plugin(OrderedDict):
    """ Plugin """

    def __init__(self, name, library, config):
        super(Plugin, self).__init__()
        self["name"] = name
        self["library"] = library
        self["config"] = config
        self["filename"] = name+".yaml"

    @property
    def name(self):
        """ Name """
        return self["name"]

    @property
    def library(self):
        """ Library """
        return self["library"]

    @property
    def config(self):
        """ Config """
        return self["config"]

    @property
    def filename(self):
        """ Filename """
        return self["filename"]


class Plugins(list):
    """ Plugins """

    def __init__(self, gait, control_parameters):
        super(Plugins, self).__init__()
        self.gait = gait
        # Control
        self.append(
            Plugin(
                name="control",
                library="libbiorob_salamander_control2_plugin.so",
                config=control_parameters.data()
            )
        )
        if gait == "swimming":
            self.append(
                Plugin(
                    name="viscous_swimming",
                    library="libbiorob_salamander_viscous_swimming_plugin.so",
                    config={"swimming_parameter": True}
                )
            )
        self.append(
            Plugin(
                name="log_kinematics",
                library="libbiorob_salamander_log_kinematics_plugin.so",
                config={
                    "filename": "logs/links_kinematics.pbdat",
                    "links": OrderedDict(
                        [
                            (
                                "link_body_{}".format(i),
                                {"frequency": 100 if i == 0 else 10}
                            )
                            for i in range(12)
                        ]
                    )
                }
            )
        )


class Package(OrderedDict):
    """ Model package """

    def __init__(self, creator, model, path=".gazebo/models/"):
        super(Package, self).__init__()
        self["creator"] = creator
        self["model"] = model
        self["path"] = path

    @property
    def creator(self):
        """ Creator """
        return self["creator"]

    @property
    def model(self):
        """ Model """
        return self["model"]

    @property
    def path(self):
        """ Path """
        return self["path"]

    def generate(self):
        """ Generate """


def generate_model_options(name, base_model, gait, control_parameters):
    """ Generate package """
    creator = Creator(
        name="Jonathan Arreguit",
        email="jonathan.arreguitoneill@epfl.ch"
    )
    plugins = Plugins(gait, control_parameters)
    model = Model(
        name=name,
        base_model=base_model,
        plugins=plugins,
        version="0.1"
    )
    package = Package(
        creator=creator,
        model=model,
        path=".gazebo/models/"
    )
    return package


def generate_walking(name, control_parameters):
    """ Generate walking salamander """
    package = generate_model_options(
        name=name,
        base_model="biorob_salamander",
        gait="walking",
        control_parameters=control_parameters
    )
    templates = ModelGenerationTemplates()
    templates.render(package)


def generate_swimming(name, control_parameters):
    """ Generate walking salamander """
    package = generate_model_options(
        name=name,
        base_model="biorob_salamander_slip",
        gait="swimming",
        control_parameters=control_parameters
    )
    templates = ModelGenerationTemplates()
    templates.render(package)


def generate_all():
    """ Test entity generation """
    name = "salamander_new"
    generate_walking(
        name,
        ControlParameters(gait="walking", frequency=1)
    )
    generate_walking(
        name+"_slow",
        ControlParameters(gait="walking", frequency=0.5)
    )
    generate_walking(
        name+"_fast",
        ControlParameters(gait="walking", frequency=2)
    )
    generate_swimming(
        "salamander_swimming",
        ControlParameters(gait="swimming", frequency=2)
    )


if __name__ == '__main__':
    generate_all()
