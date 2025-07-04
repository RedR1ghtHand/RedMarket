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
* [![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* [![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="features"></a>
## ⚡ Features

- **Smart Search Panel:**  
  Enhanced search with material-related aliases. For example, typing "wood" or "stone" suggests relevant item types automatically.
  
- **Order Detail View:**  
  Shows seller info, material (if applicable), enchantments, price, quantity, and a dynamic "Buy" button that copies a ready-to-use trade message to clipboard for quick in-game pasting.

- **User Public Profile:**  
  Displays user’s orders and social features like reputation (give or report) and built-in messaging.

- **Flexible Filtering and Sorting:**  
  Both order and user detail views support sorting by price or quantity, filtering by material or category, and prefetch related enchantments for performance.

- **User Profile:**  
  Personalized profile pages with intuitive navigation for managing account settings, orders, reputations, and direct messages.

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
- Simple built-in messaging with a chat window and conversation list.  

</details>

*Note: This is a brief overview of the core components. A more detailed technical documentation and usage guide is currently in progress and will be available soon via an external link.*
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="acks"></a>
### 🙏 Acknowledgments

Amazing technologies and tools that make this project possible:

* [![Poetry](https://img.shields.io/badge/Poetry-1.8.0-blue?style=for-the-badge&logo=python&logoColor=white)](https://python-poetry.org/)
* [![Django](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
* [![Django Extensions](https://img.shields.io/badge/Django--Extensions-4.1+-green?style=for-the-badge)](https://django-extensions.readthedocs.io/)
* [![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1.0-black?style=for-the-badge)](https://gunicorn.org/)
* [![Docker](https://img.shields.io/badge/Docker-20.10.24-blue?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
* [![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

A big shoutout to the [Best README Template](https://github.com/othneildrew/Best-README-Template) by othneildrew for the awesome README inspiration!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### License

This project is licensed under a custom **Non-Commercial License**.  
You may use it for learning and educational purposes only.  
Commercial use is strictly prohibited. See the [LICENSE](./LICENSE.txt) file for details.



