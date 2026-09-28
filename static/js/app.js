document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       MOBILE SIDEBAR
       ===================================================== */

    const mobileMenuButton =
        document.getElementById("mobileMenuButton");

    const sidebar =
        document.getElementById("sidebar");


    if (mobileMenuButton && sidebar) {

        /* -----------------------------------------------
           Open / Close with hamburger button
           ----------------------------------------------- */

        mobileMenuButton.addEventListener("click", function (event) {

            event.stopPropagation();

            sidebar.classList.toggle("sidebar-open");

        });


        /* -----------------------------------------------
           Close when clicking outside sidebar
           ----------------------------------------------- */

        document.addEventListener("click", function (event) {

            const clickedInsideSidebar =
                sidebar.contains(event.target);

            const clickedMenuButton =
                mobileMenuButton.contains(event.target);


            if (
                sidebar.classList.contains("sidebar-open") &&
                !clickedInsideSidebar &&
                !clickedMenuButton
            ) {

                sidebar.classList.remove("sidebar-open");

            }

        });


        /* -----------------------------------------------
           Close when pressing Escape
           ----------------------------------------------- */

        document.addEventListener("keydown", function (event) {

            if (event.key === "Escape") {

                sidebar.classList.remove("sidebar-open");

            }

        });


        /* -----------------------------------------------
           Close after clicking a sidebar navigation link
           ----------------------------------------------- */

        const sidebarLinks =
            sidebar.querySelectorAll("a");

        sidebarLinks.forEach(function (link) {

            link.addEventListener("click", function () {

                sidebar.classList.remove("sidebar-open");

            });

        });

    }


    /* =====================================================
       PASSWORD VISIBILITY TOGGLE
       ===================================================== */

    function setupPasswordToggle(
        passwordInputId,
        toggleButtonId
    ) {

        const passwordInput =
            document.getElementById(passwordInputId);

        const toggleButton =
            document.getElementById(toggleButtonId);


        if (
            !passwordInput ||
            !toggleButton
        ) {

            return;

        }


        toggleButton.addEventListener(
            "click",
            function () {

                if (
                    passwordInput.type === "password"
                ) {

                    passwordInput.type = "text";

                    toggleButton.textContent = "🙈";

                    toggleButton.setAttribute(
                        "aria-label",
                        "Hide password"
                    );

                    toggleButton.setAttribute(
                        "title",
                        "Hide password"
                    );

                } else {

                    passwordInput.type = "password";

                    toggleButton.textContent = "👁";

                    toggleButton.setAttribute(
                        "aria-label",
                        "Show password"
                    );

                    toggleButton.setAttribute(
                        "title",
                        "Show password"
                    );

                }

            }
        );

    }


    setupPasswordToggle(
        "id_password",
        "passwordToggle"
    );

    setupPasswordToggle(
        "id_password1",
        "password1Toggle"
    );

    setupPasswordToggle(
        "id_password2",
        "password2Toggle"
    );

});