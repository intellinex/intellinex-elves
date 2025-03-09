
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

    
    
    render() {
        const path = window.location.pathname;
        const current_page = path.split("/");
        console.log("Current Page:", current_page);
        this.container.innerHTML = `
            <aside class="c_sidebar d-flex flex-column justify-content-between" id="c_sidebar">


                <div>

                    <div class="d-flex flex-row align-items-center justify-content-between mb-3">
                        <div class="d-flex flex-row gap-2">
                            <img src="/static/assets/favicon.png" style="border-radius: 6px;" width="40"
                                height="40">
                            <div class="d-flex flex-column">
                                <span class="fw-semibold">INTELLINEX</span>
                                <span class="fw-medium" style="font-size: 12px; margin-top: -3px;">Admin Panel</span>
                            </div>
                        </div>

                        <div>
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="lucide lucide-chevrons-down-up">
                                <path d="m7 20 5-5 5 5"/>
                                <path d="m7 4 5 5 5-5"/>
                            </svg>
                        </div>

                    </div>


                     <nav>
                        <ul class="c_nav">
                            <li>
                                <a href="/admin"
                                class="d-flex flex-row align-items-center justify-content-between ${current_page[1] == 'admin' ? 'active' : ''}"
                                aria-current="page">
                                    <div class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                                            stroke-linejoin="round"
                                            class="lucide lucide-layout-dashboard">
                                            <rect width="7" height="9" x="3" y="3" rx="1"/>
                                            <rect width="7" height="5" x="14" y="3" rx="1"/>
                                            <rect width="7" height="9" x="14" y="12" rx="1"/>
                                            <rect width="7" height="5" x="3" y="16" rx="1"/>
                                        </svg>
                                        <span>Dashboard</span>
                                    </div>
                                </a>
                            </li>
                        </ul>
                     </nav>


                    <nav>
                        <span class="c_label">Platform</span>
                        <ul class="c_nav">
                            <li>
                                <a href="/author/platform/company/list"
                                class="d-flex flex-row align-items-center justify-content-between ${current_page[3] == 'company' ? 'active' : ''}"
                                aria-current="page">
                                    <div class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                            stroke-linejoin="round" class="lucide lucide-building">
                                            <rect width="16" height="20" x="4" y="2" rx="2" ry="2"/>
                                            <path d="M9 22v-4h6v4"/>
                                            <path d="M8 6h.01"/>
                                            <path d="M16 6h.01"/>
                                            <path d="M12 6h.01"/>
                                            <path d="M12 10h.01"/>
                                            <path d="M12 14h.01"/>
                                            <path d="M16 10h.01"/>
                                            <path d="M16 14h.01"/>
                                            <path d="M8 10h.01"/>
                                            <path d="M8 14h.01"/>
                                        </svg>
                                        <span>Company</span>
                                    </div>
                                    <!--<div>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                            stroke-linejoin="round" class="lucide lucide-chevron-right">
                                            <path d="m9 18 6-6-6-6"/>
                                        </svg>
                                    </div> -->
                                </a>
                            </li>

                            <li>
                                <a href="/author/platform/job/list"
                                class="d-flex flex-row align-items-center justify-content-between ${current_page[3] == "job" ? 'active' : ''} "
                                aria-current="page">
                                    <div class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                            stroke-linejoin="round" class="lucide lucide-briefcase-business">
                                            <path d="M12 12h.01"/>
                                            <path d="M16 6V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
                                            <path d="M22 13a18.15 18.15 0 0 1-20 0"/>
                                            <rect width="20" height="14" x="2" y="6" rx="2"/>
                                        </svg>
                                        <span>Job Posting</span>
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
                                    <!-- <div>
                                       <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gallery-vertical-end"><path d="M7 2h10"/><path d="M5 6h14"/><rect width="18" height="12" x="3" y="10" rx="2"/></svg>
                                    </div> -->
                                </a>
                            </li>

                        </ul>
                    </nav>




                    <nav>
                        <span class="c_label">Auth</span>

                        <ul class="c_nav">
                            <li>
                                <a href="#" id="user" class="d-flex flex-row align-items-center justify-content-between ${current_page[3] == 'user' ? 'active' : ''}"
                                aria-current="page">
                                    <div class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                            stroke-linejoin="round" class="lucide lucide-contact">
                                            <path d="M16 2v2"/>
                                            <path d="M7 22v-2a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2"/>
                                            <path d="M8 2v2"/>
                                            <circle cx="12" cy="11" r="3"/>
                                            <rect x="3" y="4" width="18" height="18" rx="2"/>
                                        </svg>
                                        <span>Auth</span>
                                    </div>
                                    <div class="dropdown-arrow" >
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                            stroke-linejoin="round" class="lucide lucide-chevron-right">
                                            <path d="m9 18 6-6-6-6"/>
                                        </svg>
                                    </div>
                                </a>

                                <!-- Dropdown Menu -->
                                <ul class="c_dropdown_menu">
                                    <li><a href="/author/auth/user/list" class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                                            stroke-linejoin="round"
                                            class="lucide lucide-user">
                                            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                                            <circle cx="12" cy="7" r="4"/>
                                        </svg>
                                        <span>User</span>
                                    </a></li>
                                    <li><a href="#" class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                                            stroke-linejoin="round"
                                            class="lucide lucide-settings">
                                            <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                                            <circle cx="12" cy="12" r="3"/>
                                        </svg>
                                        <span>Roles</span>
                                    </a></li>
                                    <li><a href="#" class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                                            stroke-linejoin="round"
                                            class="lucide lucide-settings">
                                            <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                                            <circle cx="12" cy="12" r="3"/>
                                        </svg>
                                        <span>Group</span>
                                    </a></li>
                                </ul>


                            </li>
                        </ul>

                    </nav>




                    <nav style="margin-top: 12px;" >
                        <span class="c_label">Configuration</span>
                        <ul class="c_nav">
                            <li>
                                <a href="/author/config/location/list" class="d-flex flex-row align-items-center justify-content-between {{ 'active' if current_page == 'location' else '' }}"
                                aria-current="page">
                                    <div class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                            stroke-linejoin="round" class="lucide lucide-map-pinned">
                                            <path d="M18 8c0 3.613-3.869 7.429-5.393 8.795a1 1 0 0 1-1.214 0C9.87 15.429 6 11.613 6 8a6 6 0 0 1 12 0"/>
                                            <circle cx="12" cy="8" r="2"/>
                                            <path d="M8.714 14h-3.71a1 1 0 0 0-.948.683l-2.004 6A1 1 0 0 0 3 22h18a1 1 0 0 0 .948-1.316l-2-6a1 1 0 0 0-.949-.684h-3.712"/>
                                        </svg>
                                        <span>Location</span>
                                    </div>
                                </a>
                            </li>

                            <li>
                                <a href="/author/config/employment_type/list" class="d-flex flex-row align-items-center justify-content-between {{ 'active' if current_page == 'location' else '' }}"
                                aria-current="page">
                                    <div class="d-flex align-items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-briefcase-conveyor-belt"><path d="M10 20v2"/><path d="M14 20v2"/><path d="M18 20v2"/><path d="M21 20H3"/><path d="M6 20v2"/><path d="M8 16V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v12"/><rect x="4" y="6" width="16" height="10" rx="2"/></svg>
                                        <span>Employment Type</span>
                                    </div>
                                </a>
                            </li>
                        </ul>
                    </nav>
                </div>

                <div class="">
                    <div>
                        <div>
                            <span>Chenter PHAI</span>
                        </div>
                    </div>
                </div>

            </aside>
        `;
        this.addEventListeners();
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
                    <a href="#" class="notification" aria-label="Notifications">
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