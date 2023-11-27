import yaml

class Config:
    def __init__(self, base_url, articles_dir, time_interval):
        self.base_url = base_url
        self.articles_dir = articles_dir
        self.time_interval = time_interval

    @classmethod
    def init_by_conf(cls, config_path):
        print("tomer"+ config_path)
        with open(config_path, 'r') as f:
            config_file = yaml.safe_load(f)
            base_url = config_file.get('base_url')
            articles_dir = config_file.get('articles_dir')
            time_interval = config_file.get('time_interval')
            return cls(base_url, articles_dir, time_interval)
