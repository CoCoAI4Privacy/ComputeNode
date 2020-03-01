from lifecycle_handler import Lifecycle

lifecycle = Lifecycle("all")
lifecycle.start("all")
lifecycle.wait_for_exit()