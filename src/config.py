import os
import configparser

class Config:
    def __init__(self):
        self.file = './src/config.ini' 
        self.config = configparser.RawConfigParser(allow_no_value=True)
        self.init()

    def init(self):
        if not os.path.exists(self.file):
            self.create_config()
        self.config.read(self.file)

    def create_config(self):
        # Create the configuration file as it doesn't exist yet
        # os.chmod(self.file, stat.S_IRWXO) 
        cfgfile = open(self.file, "w")
        # Add content to the file
        Config = configparser.ConfigParser()
        Config.add_section("settings")
        Config.set("settings", "Rules Path", "./src/snort3-community.rules")

        Config.write(cfgfile)
        cfgfile.close()

    def _get(self, section, key):
        return self.config[section][key]

    def _set(self, section, key, value):
        self.config[section][key] = value
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)


Config().create_config()