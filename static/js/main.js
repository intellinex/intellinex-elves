
const path = window.location.pathname.replace(/\/$/, '');

class Component {

    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }
    async loadNavItem(file, targetId) {
        try {
            const response = await fetch(file);
            if (!response.ok) throw new Error(`Failed to load ${file}: ${response.statusText}`);
            let html = await response.text();
            const folderName = file.split('/').slice(-2, -1)[0];
            const isActive = path.split("/")[1] === folderName;
            html = html.replace('{{current_page}}', isActive ? 'active' : '');
            document.getElementById(targetId).insertAdjacentHTML('beforeend', html);
        } catch (error) {
            console.error(error);
        }
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

        this.container.innerHTML = `
            <aside class="c_sidebar d-flex flex-column justify-content-between" id="c_sidebar">
                <div>
                    <div id="sidebar-header"></div>
                    
                    <!-- Default Dashboard -->
                    <nav>
                        <ul class="c_nav" id="dashboard"></ul>
                    </nav>

                    <!-- GROUP Authentication -->
                    <nav>
                        <span class="c_label">Auth</span>
                        <ul class="c_nav" id="auth-nav"></ul>
                    </nav>
                    
                    <!-- GROUP Platform -->
                    <nav>
                        <span class="c_label">Platform</span>
                        <ul class="c_nav" id="platform-nav"></ul>
                    </nav>
            
                    <!-- GROUP Product -->
                    <nav>
                        <span class="c_label">Product</span>
                        <ul class="c_nav" id="product-nav"></ul>
                    </nav>
            
                    <!-- GROUP Payment -->
                    <nav>
                        <span class="c_label">Payment</span>
                        <ul class="c_nav" id="payment-nav"></ul>
                    </nav>
            <!-- Customize Layout -->

                </div>

                <div class="" id="sidebar-footer"></div>

            </aside>
        `;

        await this.loadNavItem('/static/components/admin/page.html', 'dashboard');
        await this.loadNavItem('/static/components/user/menu.html', 'auth-nav');
        await this.loadNavItem('/static/components/admin/header.html', 'sidebar-header');
        await this.loadNavItem('/static/components/admin/footer.html', 'sidebar-footer');
        await this.loadNavItem('/static/components/platform/menu.html', 'platform-nav');
        await this.loadNavItem('/static/components/product/menu.html', 'product-nav');
        
        await this.loadNavItem('/static/components/payment/menu.html', 'payment-nav');
            this.addEventListeners();
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        $(document).ready(function () {

            // Dropdown logic
            $("#user").click(function (e) {
                e.preventDefault();
                e.stopPropagation();
                $(this).siblings("#c_dropdown_menu_user").slideToggle(400);
                $(this).find("#dropdown-arrow-user").toggleClass("active");
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
        const path = window.location.pathname.replace(/\/$/, '');
        const current_page = path.split("/");
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

                    <div class="c_breadcrumb">
                        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#888888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-house"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
                        ${current_page.slice(1).map((item) => {
                            return `
                            <div>
                                <span style="font-size: 10px; color: #888888;" >/</span>
                                <span style="font-size: 13px; color: #888888; text-transform: capitalize;" >
                                    ${item}
                                </span>
                            </div>
                            `
                        })}
                    </div>

                </div>

                <div class="header-right">
                    <a href="/notification" class="notification" aria-label="Notifications">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="#333333" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bell-ring"><path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M22 8c0-2.3-.8-4.3-2-6"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/><path d="M4 2C2.8 3.7 2 5.7 2 8"/></svg>
                        <span style="font-size: 13px; margin-left: 4px;">Notification</span>
                    </a>
                    <a href="/profile" class="user-profile" aria-label="User Profile">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-user-round"><path d="M18 20a6 6 0 0 0-12 0"/><circle cx="12" cy="10" r="4"/><circle cx="12" cy="12" r="10"/></svg></a>
                </div>
            </header>
        `;
    }
}


class ActionContainer extends Component {
    constructor(containerId) {
        super(containerId);
    }
    async render() {
        this.container.innerHTML = `
          <div id="table-bar-action"></div>  
        `;

        await this.loadNavItem('/static/components/admin/table-bar-action.html', 'table-bar-action');

        this.addEventListeners();
    }
    addEventListeners() {
        const addButton = this.container.querySelector("#add-button");
        addButton.addEventListener("click", () => {
            console.log("Add button clicked!");
            // Add your logic here
        });

        const editButton = this.container.querySelector("#edit-button");
        editButton.addEventListener("click", () => {
            console.log("Edit button clicked!");
            // Add your logic here
        });

        const deleteButton = this.container.querySelector("#delete-button");
        deleteButton.addEventListener("click", () => {
            console.log("Delete button clicked!");
            // Add your logic here
        });

        const moreButton = this.container.querySelector("#more-button");
        moreButton.addEventListener("click", () => {
            console.log("More button clicked!");
            // Add your logic here
        });
    }
}


class Dashboard {
    constructor() {
        this.sidebar = new Sidebar("sidebar-container");
        this.header = new Header("header-container");
        this.action = new ActionContainer('table-action-container');
    }

    initialize() {
        this.sidebar.render();
        this.header.render();
        console.log(path.split("/")[1])
        if(path.split("/")[1] !== "admin") {
            this.action.render();
        }
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
    });
  
    $(document).click(function (e) {
      if (!$(e.target).closest("#c_sidebar").length && !$(e.target).is(".menu_icon")) {
        $("#c_sidebar").removeClass("active");
      }
    });
});