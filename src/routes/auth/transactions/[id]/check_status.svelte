<script>
    import backgroundImage from '$lib/assets/page-background.png';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { verify_transaction } from '$lib/firebase/registrationDetails';
    import { getApp, initializeApp } from 'firebase/app';
    const dev = true;
    import firebaseConfig from '$lib/firebase/firebaseConfig';
    import { getAuth } from 'firebase/auth';
    import { getFirestore } from 'firebase/firestore/lite';
    let page_text = 'Please wait';
    let app;
    let auth;
    let db;
    let details;
    let verify
    let dataPromiseResolve;
    let dataPromise = new Promise((resolve) => {
        dataPromiseResolve = resolve;
    });
    onMount(async () => {
        try {
            app = getApp();
        } catch (error) {
            dev ? console.log('getApp: error', error) : '';
            // This means the app is not yet intialized.
            app = initializeApp(firebaseConfig);
        }
        // Now we for sure have an app.
        dev ? console.log(app) : '';
        // Redirect Handler, used when the user is authenticated.
        auth = getAuth();
        db = getFirestore();
        const _verify = await fetch(`/auth/transactions/${$page.params.id}/verify`);
        verify = await _verify.json();
        if (verify?.order_status == 'PAID') {
            page_text =
                'Payment has been sucessfully recieved. Please view and keep the reciept safely. You may return to dashboard.';
            verify_transaction(app, db, $page.params.id);
        } else {
            page_text =
                'Payment has not been successfully recieved. Please try again. Please contact support if the issue persists';
        }
        dataPromiseResolve(verify);
    });
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
                class="tw-card tw-w-96 tw-flex-shrink-0 tw-bg-base-100 tw-bg-opacity-75 tw-shadow-2xl tw-backdrop-blur"
            >
                <div class="tw-card-body">
                    <h1 class="tw-my-4 tw-text-left tw-text-xl">Verifying Payment Status</h1>
                    <span class="tw-my-2 tw-text-left tw-text-sm">{page_text}</span>
                    <hr class="tw-my-2 tw-hidden tw-border-b tw-border-gray-600 " />
                    <span class="tw-text-left"></span>
                    <div class="tw-mt-4 tw-flex tw-flex-col tw-items-center tw-justify-center">
                        {#await dataPromise then value}
                        {#if verify?.order_status == 'PAID'}
                        <a
                        sveltekit:prefetch
                        href="/dashboard/registration/{$page.params.id}/view"
                        class="tw-btn-neutral-primary tw-btn tw-mb-4"
                    >
                        <span class="tw-inner-text tw-btn">View Reciept</span>
                    </a>
                        {/if}
                            <a
                                sveltekit:prefetch
                                href="/dashboard"
                                class="tw-btn-neutral-primary tw-btn"
                            >
                                <span class="tw-inner-text tw-btn">Return To Dashboard</span>
                            </a>
                        {/await}
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>
