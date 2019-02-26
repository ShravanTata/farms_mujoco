"""Generate base"""


import os

from xml.etree import ElementTree as etree

from .model import (
    generate_model_options,
    ModelGenerationTemplates
)
from .sdf_utils import new_sdf_text


class FrictionParameters:
    """FrictionParameters"""

    def __init__(self, body, feet):
        super(FrictionParameters, self).__init__()
        self._body = body
        self._feet = feet

    @property
    def feet(self):
        """Feet"""
        return self._feet

    @property
    def body(self):
        """Body"""
        return self._body


def apply_collisions_properties(root, friction_params, verbose=False):
    """Apply collisions properties"""
    for collision in root.iter('collision'):
        if verbose:
            print("collision: {}".format(collision))
            print("tag: {} attribute: {}".format(collision.tag, collision.attrib))
        if "name" in collision.attrib:
            max_contacts = etree.Element("max_contacts")
            max_contacts.text = str(3)
            collision.append(max_contacts)
            surface = etree.Element("surface")
            collision.append(surface)
            # Friction
            friction = etree.Element("friction")
            surface.append(friction)
            # torsional = etree.Element("torsional")
            # friction.append(torsional)
            # coefficient = etree.Element("coefficient")
            # coefficient.text = str(friction_mu)
            # torsional.append(coefficient)
            # # ODE
            # ode = etree.Element("ode")
            # friction.append(ode)
            # mu = etree.Element("mu")
            # mu.text = str(friction_params.feet)
            # ode.append(mu)
            # mu2 = etree.Element("mu2")
            # mu2.text = str(friction_params.feet)
            # ode.append(mu2)
            # # Bounce
            # bounce = etree.Element("bounce")
            # surface.append(bounce)
            # restitution_coefficient = etree.Element("restitution_coefficient")
            # restitution_coefficient.text = str(0)
            # bounce.append(restitution_coefficient)
            # threshold = etree.Element("threshold")
            # threshold.text = str(0)
            # bounce.append(threshold)
            # # Contact
            # contact = etree.Element("contact")
            # surface.append(contact)
            # ode = etree.Element("ode")
            # contact.append(ode)
            # soft_cfm = etree.Element("soft_cfm")
            # soft_cfm.text = str(0)
            # ode.append(soft_cfm)
            # soft_erp = etree.Element("soft_erp")
            # soft_erp.text = str(0.2)
            # ode.append(soft_erp)
            # kp = etree.Element("kp")
            # kp.text = str(1e6)
            # ode.append(kp)
            # kd = etree.Element("kd")
            # kd.text = str(1e2)
            # ode.append(kd)
            # max_vel = etree.Element("max_vel")
            # max_vel.text = str(0.01)
            # ode.append(max_vel)
            # min_depth = etree.Element("min_depth")
            # min_depth.text = str(1e2)
            # ode.append(min_depth)
            # Bullet
            bullet = etree.Element("bullet")
            friction.append(bullet)
            friction = etree.Element("friction")
            friction.text = str(friction_params.feet)
            bullet.append(friction)
            friction2 = etree.Element("friction2")
            friction2.text = str(friction_params.feet)
            bullet.append(friction2)
            # Bounce
            bounce = etree.Element("bounce")
            surface.append(bounce)
            restitution_coefficient = etree.Element("restitution_coefficient")
            restitution_coefficient.text = str(0)
            bounce.append(restitution_coefficient)
            threshold = etree.Element("threshold")
            threshold.text = str(100000)
            bounce.append(threshold)
            # Contact
            contact = etree.Element("contact")
            surface.append(contact)
            bullet = etree.Element("bullet")
            contact.append(bullet)
            soft_cfm = etree.Element("soft_cfm")
            soft_cfm.text = str(0)
            bullet.append(soft_cfm)
            soft_erp = etree.Element("soft_erp")
            soft_erp.text = str(0.2)
            bullet.append(soft_erp)
            kp = etree.Element("kp")
            kp.text = str(1e0)  # 1e6
            bullet.append(kp)
            kd = etree.Element("kd")
            kd.text = str(1e0)  # 1e2
            bullet.append(kd)
            max_vel = etree.Element("split_impulse")
            max_vel.text = str(1)
            bullet.append(max_vel)
            min_depth = etree.Element("split_impulse_penetration_threshold")
            min_depth.text = str(-0.01)
            bullet.append(min_depth)



def add_contact_sensors(root, verbose=False):
    """Apply collisions properties"""
    for link in root.iter('link'):
        if verbose:
            print("link: {}".format(link))
        if "name" in link.attrib:
            if "_R_3" in link.attrib["name"] or "_L_3" in link.attrib["name"]:
                if verbose:
                    print("Foot found: {}".format(link.attrib["name"]))
                sensor = etree.Element("sensor")
                sensor.attrib["name"] = "sensor_{}_{}".format(
                    "contact",
                    link.attrib["name"]
                )
                sensor.attrib["type"] = "contact"
                link.append(sensor)
                always_on = etree.Element("always_on")
                always_on.text = "true"
                sensor.append(always_on)
                update_rate = etree.Element("update_rate")
                update_rate.text = "1000"
                sensor.append(update_rate)
                visualize = etree.Element("visualize")
                visualize.text = "true"
                sensor.append(visualize)
                # topic = etree.Element("topic")
                # topic.text = "__default__"
                # sensor.append(topic)
                contact = etree.Element("contact")
                sensor.append(contact)
                collision = etree.Element("collision")
                collision.text = "__default__"
                contact.append(collision)
                # topic = etree.Element("topic")
                # topic.text = "__default_topic__"
                # contact.append(topic)


def correct_joint_names(root, verbose=False):
    """Correct joint names"""
    for joint in root.iter('joint'):
        if verbose:
            print("joint: {}".format(joint))
        joint.attrib["name"] = "joint_"+joint.attrib["name"]


def add_joint_dynamics(root, verbose=False):
    """Apply collisions properties"""
    for joint in root.iter('joint'):
        if verbose:
            print("joint: {}".format(joint))
        if joint.attrib["type"] == "revolute":
            for axis in joint.iter('axis'):
                dynamics = etree.Element("dynamics")
                axis.append(dynamics)
                damping = etree.Element("damping")
                damping.text = "0.1"
                dynamics.append(damping)
                friction = etree.Element("friction")
                friction.text = "0"
                dynamics.append(friction)
                spring_reference = etree.Element("spring_reference")
                spring_reference.text = "0"
                dynamics.append(spring_reference)
                spring_stiffness = etree.Element("spring_stiffness")
                spring_stiffness.text = "0.1"
                dynamics.append(spring_stiffness)


def add_force_torque_sensors(root, verbose=False):
    """Apply collisions properties"""
    for joint in root.iter('joint'):
        if verbose:
            print("joint: {}".format(joint))
        if "_R_3" in joint.attrib["name"] or "_L_3" in joint.attrib["name"]:
            if verbose:
                print("Ankle found: {}".format(joint.attrib["name"]))
            sensor = etree.Element("sensor")
            sensor.attrib["name"] = "sensor_{}_{}".format(
                "ft",
                joint.attrib["name"]
            )
            sensor.attrib["type"] = "force_torque"
            joint.append(sensor)
            always_on = etree.Element("always_on")
            always_on.text = "true"
            sensor.append(always_on)
            update_rate = etree.Element("update_rate")
            update_rate.text = "1000"
            sensor.append(update_rate)
            visualize = etree.Element("visualize")
            visualize.text = "true"
            sensor.append(visualize)
            # topic = etree.Element("topic")
            # topic.text = "__default__"
            # sensor.append(topic)
            force_torque = etree.Element("force_torque")
            sensor.append(force_torque)
            frame = etree.Element("frame")
            frame.text = "sensor"
            force_torque.append(frame)
            measure_direction = etree.Element("measure_direction")
            measure_direction.text = "child_to_parent"
            force_torque.append(measure_direction)


def correct_sdf_visuals_materials(root):
    """Correct materials from SDF visuals (DEPRECATED)

    Gazebo currently does not support obtaining materials from SDF directly. As
    the material incformation is encoded inside the COLLADA files, the material
    information obtained from the SDF file can be removed.

    """
    # Correct visuals materials (Gazebo/SDF does not fully support specular)
    for visual in root.iter('visual'):
        for stuff in visual.findall('material'):
            visual.remove(stuff)
    return root


def create_new_model(previous_model, new_model, friction):
    """Create new model from previous model"""
    home = os.path.expanduser("~")
    path_models = home + "/.gazebo/models/"
    path_model_previous = path_models+"{}/".format(previous_model)
    path_sdf_previous = path_model_previous+"{}.sdf".format(previous_model)
    # path_model_new = path_models+"{}/".format(new_model)
    # path_sdf_new = path_model_new+"{}.sdf".format(new_model)

    # SDF
    tree = etree.parse(path_sdf_previous)
    root = tree.getroot()

    # Correct joints
    correct_joint_names(root)

    # Apply joints dynamics
    add_joint_dynamics(root)

    # Collision properties
    apply_collisions_properties(root, friction)

    # Add sensors
    add_contact_sensors(root)
    add_force_torque_sensors(root)

    # Write to SDF
    sdf = new_sdf_text(root)

    # Generate package
    package = generate_model_options(
        name=new_model,
        base_model=previous_model
    )
    templates = ModelGenerationTemplates()
    packager = templates.render(package, sdf=sdf)
    packager.generate()


def generate_base():
    """Generate base models"""
    model_names = [
        "biorob_salamander_base",
        "biorob_salamander_base_slip",
        "biorob_salamander_base_slip_no_legs",
        "biorob_centipede_base",
        "biorob_polypterus_base"
    ]
    for model_name in model_names:
        previous_model = "{}".format(model_name)
        next_model = "{}".format(model_name.replace("_base", ""))
        friction = FrictionParameters(body=1e-3, feet=0.7)
        create_new_model(previous_model, next_model, friction)
