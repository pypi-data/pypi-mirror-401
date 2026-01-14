class Config: 
    """
    Global configuration for nsx. 
    Default Logic: 'product' (Best for Deep Learning)
    """
    _instance = None 

    def __new__(cls):
        if cls._instance is None: 
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.logic_type = "product"
        return cls._instance

    @property
    def logic(self):
        return self.logic_type 

    @logic.setter
    def logic(self, value):
        if value not in ["product", "godel", "lukasiewicz", "log_product"]:
            raise ValueError(f"Unknown logic type: {value}")
        self.logic_type = value


# Global instance for easy access 
conf = Config()

