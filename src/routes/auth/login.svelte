<script lang="ts">
    import Icon from '@iconify/svelte/dist/OfflineIcon.svelte';
    import GitHubIcon from '@iconify-icons/simple-icons/github.js';
    import GoogleIcon from '@iconify-icons/simple-icons/google.js';
    import Eye from '@iconify-icons/ic/outline-remove-red-eye.js';
    import { dev } from '$app/env';

    // function for password show/hide
    let is_password_shown = false;
    function password_toggle(event) {
        if (dev) {
            console.log('password_toggle', event);
        }
        is_password_shown = !is_password_shown;
    }

    // function for username validation
    let email_input = '';
    let email_error = '';
    function email_on_blur(event) {
        if (dev) {
            console.log('email_on_blur', event);
        }
        
        const emailRegex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        
        if (email_input.length < 1) {
            email_error = 'Please enter a email.';
        } else if (!email_input.includes('@')) {
            email_error = 'Please enter a valid email.';
        } else if (!emailRegex.test(email_input)) {
            email_error = 'Please enter a valid email.';
        } else {
            email_error = '';
        }
    }
    
    
    
    function username_on_blur(event) {
        if (dev) {
            console.log('username_on_blur', event);
        }
        const special_chars = /[ `!#$%^&*()+=[\]{};':"\\|,.<>/?~]/;

        if (email_input.length <= 5) {
            email_error = 'Username must be at least 6 characters long';
        } else if (email_input.length >= 20) {
            email_error = 'Username must be less than 20 characters long';
        } else if (special_chars.test(email_input)) {
            email_error =
                "Username must not contain special characters except '-' or '_' or '@' ";
        } else if (email_input.includes('@') && email_input.indexOf('@') != 0) {
            email_error =
                "If you want to use '@' in your username, please place it at the beginning";
        } else {
            email_error = '';
        }
    }

    // function for password validation
    let password_input = '';
    let password_error = '';
    function password_on_blur(event) {
        if (dev) {
            console.log('password_on_blur', event);
        }

        if (password_input.length <= 5) {
            password_error = 'Password must be at least 6 characters long';
        } else {
            password_error = '';
        }
    }

    // password input hack
    function password_on_input(event) {
        password_input = (<HTMLInputElement>event.target).value;
        password_error = '';
    }

    let is_signin_loading = false;
    function on_signin(event) {
        if (dev) {
            console.log('on_signin', event);
        }
        is_signin_loading = true;
    }

    // firebase auth login
    let is_firebase_auth_in_progress = false;
</script>

<main>
    <section class="relative w-full h-full py-40 min-h-screen">
        <div
            class="absolute top-0 w-full h-full bg-base-300 bg-no-repeat motion-safe:animate-pulse"
            style="background-image: url(&quot;/auth-bg.png&quot;);"
        />
        <div class="container mx-auto px-4 h-full">
            <div class="flex content-center items-center justify-center h-full">
                <div class="w-full lg:w-4/12 px-4">
                    <div
                        class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-base-200 border-0"
                    >
                        <div class="rounded-t mb-0 px-6 py-6">
                            <div class="text-center mb-3">
                                <span class="text-blue-100 font-bold">Sign In</span>
                            </div>
                            <div class="text-center">
                                <button class="btn bg-base-300" type="button">
                                    <Icon
                                        class="inline-block w-5 mr-2 stroke-current"
                                        icon={GitHubIcon}
                                    />
                                    Github</button
                                >
                                <button class="btn bg-base-300" type="button">
                                    <Icon
                                        class="inline-block w-5 mr-2 stroke-current"
                                        icon={GoogleIcon}
                                    />
                                    Google</button
                                >
                            </div>
                            <hr class="mt-6 border-b-1 border-primary" />
                        </div>
                        <div class="flex-auto px-4 lg:px-10 py-10 pt-0">
                            <div class="hidden text-blue-200 text-center mb-3 font-bold">
                                <small>Or Sign In With</small>
                            </div>
                            <form>
                                <div class="my-4 bg-base-200">
                                    <div class="form-control">
                                        <label for="" class="label">
                                            <span class="label-text">Email</span>
                                        </label>
                                        <input
                                            on:blur={email_on_blur}
                                            bind:value={email_input}
                                            type="email"
                                            placeholder="email@domain.tld"
                                            class="input tracking-widest font-mono {email_error
                                                ? 'border border-error'
                                                : ''}"
                                        />
                                        <label
                                            for=""
                                            class="label {email_error ? '' : 'invisible'}"
                                        >
                                            <span class="label-text-alt text-error"
                                                >{email_error
                                                    ? email_error
                                                    : 'Example String'}</span
                                            >
                                        </label>
                                    </div>
                                </div>

                                <div class="relative w-full mb-1">
                                    <div class="form-control">
                                        <label for="" class="label">
                                            <span class="label-text">Password</span>
                                            <a
                                                href="/"
                                                class="label-text-alt text-xs text-gray-400"
                                            >
                                                Need help ?
                                            </a>
                                        </label>
                                        <div class="relative">
                                            <!--Custom Hack to get reactive input type and the correct value in on_blur -->

                                            <input
                                                on:blur={password_on_blur}
                                                on:input={password_on_input}
                                                type={is_password_shown ? 'text' : 'password'}
                                                placeholder="Password"
                                                class="tracking-widest font-mono w-full pr-16 input {password_error
                                                    ? 'border border-error'
                                                    : 'Example String'}"
                                            />
                                            <button
                                                on:click|preventDefault={password_toggle}
                                                class="absolute top-0 right-0 rounded-l-none btn  {is_password_shown
                                                    ? 'btn-info'
                                                    : 'btn-ghost'} text-xs"
                                                ><Icon class="w-6 h-6" icon={Eye} /></button
                                            >
                                            <label
                                                for=""
                                                class="label {password_error ? '' : 'invisible'}"
                                            >
                                                <span class="label-text-alt text-error"
                                                    >{password_error
                                                        ? password_error
                                                        : 'Example String'}</span
                                                >
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <!-- Hidden Remember Me. We need people to login again and again. (inline-flex) -->
                                    <span class="hidden items-center cursor-pointer">
                                        <span class="ml-2 my-2 text-xs font-normal text-gray-400">
                                            Forgot Password ?</span
                                        ></span
                                    >
                                </div>

                                <div class="text-center">
                                    <button
                                        on:click={on_signin}
                                        class="btn btn-lg text-base bg-base-300 w-full {email_input
                                            ? ''
                                            : 'btn-disabled'} {password_input
                                            ? ''
                                            : 'btn-disabled'} {email_error
                                            ? 'btn-disabled'
                                            : ''} {password_error
                                            ? 'btn-disabled'
                                            : ''} {is_firebase_auth_in_progress
                                            ? 'btn-disabled'
                                            : ''} {is_signin_loading ? 'btn-disabled loading' : ''}"
                                        type="button">Sign In</button
                                    >
                                </div>
                            </form>
                        </div>
                    </div>
                    <div class="flex flex-wrap mt-6 relative">
                        <!-- Registration is closed except for special links. -->
                        <div class="w-1/2 text-right hidden">
                            <a href="/auth/register" class="text-blue-200"
                                ><small>Create new account</small></a
                            >
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</main>
