<script>
    import backgroundImage from '$lib/assets/page-background.png';
</script>

<div
    class="tw-hero tw-min-h-screen tw-bg-base-300 "
    style="background-image: url({backgroundImage});"
>
    <div
        class="tw-hero-overlay tw-bg-base-300 tw-bg-opacity-75 tw-backdrop-blur motion-safe:tw-animate-pulse"
    ></div>
    <div class="tw-hero-content tw-text-center tw-text-neutral-content">
        <form class="tw-max-w-md">
            <div
                class="tw-card tw-w-96 tw-flex-shrink-0 tw-bg-base-200 tw-bg-opacity-75 tw-shadow-2xl tw-backdrop-blur"
            >
                <div class="tw-card-body">
                    <h1 class="tw-my-4 tw-text-left tw-text-xl">Rest Easy...</h1>
                    <span class="tw-my-2 tw-text-left tw-text-sm">We have reset your password</span>
                    <hr class="tw-my-2 tw-hidden tw-border-b tw-border-gray-600 " />
                    <h2 class="tw-text-left">Please try to sign-in again</h2>
                    <div class="tw-mt-4 tw-flex tw-flex-col tw-items-center tw-justify-center">
                        <a sveltekit:prefetch href="/" class="tw-btn-neutral-primary tw-btn">
                            <span class="tw-inner-text tw-btn">Back to Home</span>
                        </a>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>
