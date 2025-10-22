name = "sanity_check"
version = "dev"

requires = []

def commands():
    global env
    global info
    global expandvars

    env.PYTHONPATH.prepend("{root}")
    info("ENTER IN {name} {version}".format(name=this.name, version=this.version))
