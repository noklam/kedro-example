from kedro.framework.hooks import hook_impl


class NokHook:
    @hook_impl
    def before_pipeline_run(self):
        print("[DEBUG] - Before pipeline Start")


nok_hook = NokHook()