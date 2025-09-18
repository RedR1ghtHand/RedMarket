<a id="readme-top"></a>

![redmarketlogo](https://github.com/user-attachments/assets/6c9ebe1d-bd31-4d25-88d0-b3fe52efbe62)

<p align="center">
  Trading platform for Minecraft players
  <br />
  <br />
  <a href="https://redmarket.click">Visit Site</a>
  &middot;
  <a href="https://github.com/RedR1ghtHand/RedMarket/issues/new?labels=bug&template=bug-report.md">Report Bug</a>
  &middot;
  <a href="https://github.com/RedR1ghtHand/RedMarket//issues/new?labels=enhancement&template=feature-request.md">Request Feature</a>
</p>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#demo">Demo</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#wiki">Wiki Docs</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acks">Acknowledgments</a></li>
  </ol>
</details>

<a id="about"></a>
## 🔎 About The Project
![redmarket](https://github.com/user-attachments/assets/d8da3054-874e-4641-b5a3-dd74e7f1f921)

RedMarket is a web-based trading platform tailored for Minecraft players. 
It provides a clean, fast interface for listing and finding item orders, 
with the entire experience centered around one core action: the Buy button. 
This button copies a prefilled message to your clipboard, so you can instantly alt+tab into the game, 
paste in chat, and kick off a trade.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="built-with"></a>
### 🧱 Built With

* [![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
* [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
* [![HTMX](https://img.shields.io/badge/HTMX-1E1E1E?style=for-the-badge&logo=htmx&logoColor=white)](https://htmx.org/)
* [![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
* [![Alpine.js](https://img.shields.io/badge/Alpine.js-8BC0D0?style=for-the-badge&logo=alpine.js&logoColor=white)](https://alpinejs.dev/)
* [![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
* [![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
* [![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryproject.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="features"></a>
## ⚡ Features

### Market
- **Order Detail View:**  
  Shows seller info, material (if applicable), enchantments, price, quantity, and a dynamic "Buy" button that copies a ready-to-use trade message to clipboard for quick in-game pasting.

- **Buy Button:**  
  Purchase process built around Minecraft in-game experience. One-click generates prefilled trade messages with commands compatible with popular chat plugins (/msg, /tell, /w). Instantly alt+tab into Minecraft, paste the message in chat, and initiate trades seamlessly.

- **Smart Search Panel:**  
  Enhanced search with material-related aliases. For example, typing "wood" or "stone" suggests relevant item types automatically.

- **Advanced Filtering & Sorting:**  
  Multi-filter support for material, category, and enchantments with sorting by price or quantity. Prefetch related enchantments for optimal performance.

### Social
- **User Status Pipeline:**  
  Real-time user status tracking with middleware for online/offline detection and last seen timestamps.

- **User Detail Pages:**  
  Comprehensive user profiles displaying orders, reputation scores, and related trading information.

- **Real-Time Messaging:**  
  WebSocket-powered instant messaging system with live chat, message notifications, and real-time updates using Django Channels.

- **Reputation System:**  
  Badge-based reputation system with positive/negative feedback options and real-time updates.

- **Notification Systems:**  
  Live notification system with toast messages, unread counts, and instant updates for messages, reputation changes, and system alerts.

- **Account Settings:**  
  Manual status control, order management, and comprehensive account configuration options.

### Modern Web Development
- **Smart Search Panel:**  
  Enhanced search with material-related aliases and intelligent suggestions.

- **Mobile-Responsive Design:**  
  Mobile-optimized detail pages with responsive layouts and touch-friendly interactions.

- **HTMX Integration:**  
  Seamless page updates without full reloads. Filter orders, load more content, and navigate between sections instantly with smooth animations.

- **Theme System:**  
  Dark/light theme toggle with persistent user preferences.

- **Background Task Processing:**  
  Celery-powered background tasks for message processing, user status updates, and notification delivery with Redis as the message broker.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="demo"></a>
## 💻 Demo
- Order creating, searching, and buy button  
![demo1](https://github.com/user-attachments/assets/9a991ad0-0b2d-4480-8d5a-f9da89c6e549)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="getting-started"></a>
## 🚀 Getting Started
<a id="getting-started"></a>
To get a local copy up and running, follow these steps.

### Prerequisites
  - [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the repo** 
   ```sh
   git clone https://github.com/RedR1ghtHand/RedMarket.git
2. **Copy env file and setup variables**  
   ```sh
   cp .env.example .env
3. **Build and start the app** 
   ```sh
   docker-compose up -d --build
4. Wait for the app to launch and visit http://localhost:8000/ (localhost must be in .env ALLOWED_HOSTS)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="wiki"></a>
## 📚 Wiki Documentation
<details>
  <summary>💎 Item Models (Business Logic)</summary>

- **Category:** Named entries with descriptions to organize items.  
- **ItemType:** Represents base item types (e.g., sword), which can be duplicated for specific materials like wooden or stone swords.  
- **Material:** Linked to ItemTypes, allowing one item type to support multiple materials, giving great flexibility (e.g., easily adding new materials like "damascus" later).  
- **Enchantments:** Highly flexible with support for dependencies, levels, and plugin-based extensions (e.g., super pickaxe with Fortune 5).  

</details>

<details>
  <summary>🛠️ Data Initialization & Admin</summary>

- Uses Django management commands to populate ItemType, Category, Material, and Enchantment from config files at setup or runtime.  
- Admin interface also supports adding and editing these core entries.  

</details>

<details>
  <summary>🛒 Order Models</summary>

- **Order:** Holds detailed data linking ItemType, Material, price, quantity, and optional custom enchantments.  
- **OrderEnchantment:** Through model linking orders and enchantments with specific levels.  
- Provides forms for creating, editing, and deleting orders via user profiles.  
- Includes mixins to support ordering and metadata across core apps.  

</details>

<details>
  <summary>💻 Account Features</summary>

- Basic user registration, login, and account settings.  
- Public profiles displaying orders and social interactions.  

</details>

<details>
  <summary>💬 Social Features</summary>

- Reputation system using badges (instead of comments) that can be configured as positive or negative in settings.  
- Real-time messaging system with WebSocket-powered instant chat, message notifications, and live updates.  
- Advanced notification system with toast messages, unread counts, and real-time delivery using Django Channels.  
- Background task processing with Celery for message handling and notification delivery.  

</details>

<details>
  <summary>⚡ Modern Frontend</summary>

- HTMX integration for seamless page updates without full reloads, providing smooth user interactions.  
- Bootstrap 5 with responsive design, dark/light theme toggle, and modern UI components.  
- Alpine.js for reactive UI elements, form handling, and smooth animations.  
- WebSocket integration for real-time features like live chat and instant notifications.  

</details>

*Note: This is a brief overview of the core components. A more detailed technical documentation and usage guide is currently in progress and will be available soon via an external link.*
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="acks"></a>
### 🙏 Acknowledgments

Amazing technologies and tools that make this project possible:

* [![Poetry](https://img.shields.io/badge/Poetry-1.8.0-blue?style=for-the-badge&logo=python&logoColor=white)](https://python-poetry.org/)
* [![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
* [![HTMX](https://img.shields.io/badge/HTMX-1.9.3-1E1E1E?style=for-the-badge&logo=htmx&logoColor=white)](https://htmx.org/)
* [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
* [![Alpine.js](https://img.shields.io/badge/Alpine.js-3.12.0-8BC0D0?style=for-the-badge&logo=alpine.js&logoColor=white)](https://alpinejs.dev/)
* [![Django Channels](https://img.shields.io/badge/Django--Channels-4.3.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://channels.readthedocs.io/)
* [![Celery](https://img.shields.io/badge/Celery-5.5.3-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryproject.org/)
* [![Redis](https://img.shields.io/badge/Redis-6.4.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
* [![Django Extensions](https://img.shields.io/badge/Django--Extensions-4.1+-green?style=for-the-badge)](https://django-extensions.readthedocs.io/)
* [![Gunicorn](https://img.shields.io/badge/Gunicorn-23.0.0-black?style=for-the-badge)](https://gunicorn.org/)
* [![Docker](https://img.shields.io/badge/Docker-20.10.24-blue?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
* [![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

A big shoutout to the [Best README Template](https://github.com/othneildrew/Best-README-Template) by othneildrew for the awesome README inspiration!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### License

This project is licensed under a custom **Non-Commercial License**.  
You may use it for learning and educational purposes only.  
Commercial use is strictly prohibited. See the [LICENSE](./LICENSE.txt) file for details.



