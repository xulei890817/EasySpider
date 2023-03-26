from ColiSpider.worker import RunTypeEnum, Worker


class PorterWorker(Worker):
    """搬运工，负责进行资源的落库"""
    ROOT_PATH = None

    def _self_check(self, *args, **kwargs):
        if self.ROOT_PATH is None:
            raise Exception("Root path must be specified")


    def _run(self, *args, **kwargs):
        pass
    

    class _Config:
        # run_type
        run_type = RunTypeEnum.PROCESS
        # use_base64
        use_base64 = False