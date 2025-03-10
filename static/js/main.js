
class Component {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }
    render() {
        throw new Error("Render method must be implemented by subclasses.");
    }
}

class Sidebar extends Component {
    constructor(containerId) {
        super(containerId);
    }

    
    
    async render() {
        const path = window.location.pathname;
        const current_page = path.split("/");
        this.container.innerHTML = `
            <aside class="c_sidebar d-flex flex-column justify-content-between" id="c_sidebar">
                <div>
                    
                    <div id="sidebar-header"></div>

                     <nav>
                        <ul class="c_nav" id="dashboard"></ul>
                     </nav>


                    <nav>
                        <span class="c_label">Platform</span>
                        <ul class="c_nav">
                            <li>
                                <a href="/author/platform/certificate/list"
                                class="d-flex flex-row align-items-center justify-content-between {{'active' if current_page == 'content' else ''}} "
                                aria-current="page">
                                    <div class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>
                                        <span>Certificate Verification</span>
                                    </div>
                                    <!-- <div>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                            stroke-linejoin="round" class="lucide lucide-chevron-right">
                                            <path d="m9 18 6-6-6-6"/>
                                        </svg>
                                    </div> -->
                                </a>
                            </li>

                            <li>
                                <a href="/author/platform/media/list"
                                class="d-flex flex-row align-items-center justify-content-between {{'active' if current_page == 'content' else ''}} "
                                aria-current="page">
                                    <div class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gallery-vertical-end"><path d="M7 2h10"/><path d="M5 6h14"/><rect width="18" height="12" x="3" y="10" rx="2"/></svg>
                                        <span>Media</span>
                                    </div>
                                </a>
                            </li>
                        </ul>
                    </nav>



                    <!-- GROUP Authentication -->
                    <nav>
                        <span class="c_label">Auth</span>
                        <ul class="c_nav" id="auth-nav"></ul>
                    </nav>

                </div>

                <div class="" id="sidebar-footer"></div>

            </aside>
        `;

        await this.loadNavItem('/static/components/admin/page.html', 'dashboard', current_page);
        await this.loadNavItem('/static/components/user/menu.html', 'auth-nav', current_page);
        await this.loadNavItem('/static/components/admin/header.html', 'sidebar-header', current_page);
        await this.loadNavItem('/static/components/admin/footer.html', 'sidebar-footer', current_page);

        this.addEventListeners();
        this.initializeEventListeners();
    }

    async loadNavItem(file, targetId, current_page) {
        try {
            const response = await fetch(file);
            if (!response.ok) throw new Error(`Failed to load ${file}: ${response.statusText}`);
            let html = await response.text();
            const folderName = file.split('/').slice(-2, -1)[0];
            const isActive = current_page[1] === folderName;
            html = html.replace('{{current_page}}', isActive ? 'active' : '');
            document.getElementById(targetId).insertAdjacentHTML('beforeend', html);
        } catch (error) {
            console.error(error);
        }
    }

    initializeEventListeners() {
        $(document).ready(function () {
            $("#user").click(function (e) {
                e.preventDefault();
                e.stopPropagation();
                $(this).siblings(".c_dropdown_menu").slideToggle(400);
                $(this).find(".dropdown-arrow").toggleClass("active");
              });
        })
    }

    addEventListeners() {
        const menuIcon = document.querySelector(".menu_icon");
        if (menuIcon) {
            menuIcon.addEventListener("click", () => {
                this.container.classList.toggle("active");
            });
        }
    }
}

class Header extends Component {
    constructor(containerId) {
        super(containerId);
    }

    render() {
        this.container.innerHTML = `
            <header class="header">
                <div class="header-left">

                    <button class="menu_icon bg-transparent d-flex align-items-center justify-content-center"
                            style="border: none; width: 20px; height: 20px;" aria-label="Toggle Sidebar">
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                                 stroke="#666666"
                                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                 class="lucide lucide-panels-top-left">
                                <rect width="18" height="18" x="3" y="3" rx="2"/>
                                <path d="M3 9h18"/>
                                <path d="M9 21V9"/>
                            </svg>
                        </span>
                    </button>


                </div>

                <div class="header-right">
                    <a href="/notification" class="notification" aria-label="Notifications">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="#333333" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bell-ring"><path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M22 8c0-2.3-.8-4.3-2-6"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/><path d="M4 2C2.8 3.7 2 5.7 2 8"/></svg>
                        <span style="font-size: 13px; margin-left: 4px;">Notification</span>
                    </a>
                    <a href="#" class="user-profile" aria-label="User Profile">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-user-round"><path d="M18 20a6 6 0 0 0-12 0"/><circle cx="12" cy="10" r="4"/><circle cx="12" cy="12" r="10"/></svg></a>
                </div>
            </header>
        `;
    }
}

class Dashboard {
    constructor() {
        this.sidebar = new Sidebar("sidebar-container");
        this.header = new Header("header-container");
    }

    initialize() {
        this.sidebar.render();
        this.header.render();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const dashboard = new Dashboard();
    dashboard.initialize();
});



$(document).ready(function () {
    $(".menu_icon").click(function (e) {
      e.stopPropagation();
      $("#c_sidebar").toggleClass("active");
      console.log('Open Side bar');
    });
  
    $(document).click(function (e) {
      if (!$(e.target).closest("#c_sidebar").length && !$(e.target).is(".menu_icon")) {
        $("#c_sidebar").removeClass("active");
        console.log("Close Side Bar")
      }
    });
});