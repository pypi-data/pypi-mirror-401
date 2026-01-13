"""Example demonstrating Sentry SDK configuration and profiling capabilities."""

import sentry_sdk

# Initialize Sentry SDK early in your application's setup
sentry_sdk.init(
    dsn="https://fb6269384565414e9c125beef9fa3787@o4510683697840128.ingest.us.sentry.io/4510683710357504",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Enable sending logs to Sentry
    enable_tracing=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of profile sessions.
    profiles_sample_rate=1.0,
)


def slow_function():
    """Simulates a slow function for profiling demonstration."""
    import time
    time.sleep(0.1)
    return "done"


def fast_function():
    """Simulates a fast function for profiling demonstration."""
    import time
    time.sleep(0.05)
    return "done"


def main():
    """Demonstrate manual profiling with Sentry."""
    print("Starting profiling demonstration...")
    
    # Manually call start_profiler and stop_profiler
    # to profile the code in between
    sentry_sdk.profiler.start_profiler()
    
    for i in range(0, 10):
        slow_function()
        fast_function()
    
    # Calls to stop_profiler are optional - if you don't stop the profiler, it will keep profiling
    # your application until the process exits or stop_profiler is called.
    sentry_sdk.profiler.stop_profiler()
    
    print("Profiling complete!")
    
    # Example: Verify setup by intentionally causing an error
    # Uncomment the following line to test error tracking:
    # division_by_zero = 1 / 0
    
    # Example: Send logs to Sentry
    import logging
    logger = logging.getLogger(__name__)
    
    # These logs will be automatically sent to Sentry
    logger.info('This is an info log message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    
    print("\nLogs sent to Sentry!")


if __name__ == "__main__":
    main()
