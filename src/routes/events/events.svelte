<script>
    const dev = true;

    import { goto } from '$app/navigation';

    import { onMount } from 'svelte';
    let scrollY = 84;
    onMount(() => {
        //scrollY = 84;
        window.onmessage = (e) => {
            dev ? console.log(e.data.toString().split(':')[1]) : '';
            if (e.data.toString().includes('%22') || e.data.toString().includes('"')) {
                return;
            }
            if (e.data.toString().includes('drafts') || e.data.toString().includes('/drafts') || e.data.toString().includes('.pdf')) {
                return;
            }
            goto(e.data.toString().split(':')[1]);
        };
    });
</script>

<svelte:head>
    <title>Adhyaaya '22</title>
</svelte:head>

<svelte:window bind:scrollY />

<!--This was a retarded attempt at trying to convert this code. Broken Click-->

<iframe
    src="/events/_index.html"
    class="tw-h-screen tw-w-screen tw-overflow-clip"
    title="Events Page, Uses external GSAP"
    frameborder="0"
></iframe>
