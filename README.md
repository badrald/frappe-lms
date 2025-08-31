### LMS - Library Management System

A comprehensive Library Management System built with Frappe Framework and Vue.js. This system allows librarians to efficiently manage books, authors, members, borrowing transactions, and generate reports.

### Features

#### Backend (Frappe Framework)

**Document Types:**
- **Book Management**: Complete CRUD operations for books with fields like title, ISBN, genre, author, publisher, and quantity tracking
- **Author Management**: Manage author information including name, biography and linked books
- **Category Management**: Organize books by categories/genres
- **Publisher Management**: Track publisher information
- **Member Management**: Register and manage library members
- **Library Membership**: Manage membership details and validity
- **Borrow/Return Transactions**: Track book borrowing and returning with due dates
- **Library Transaction**: Complete transaction history with status tracking

**API Endpoints:**
- Books API: Create, update, delete books with advanced features like cover image upload
- Authors API: Fetch and manage author information
- Categories API: Manage book categories
- Publishers API: Handle publisher data
- Reports API: Generate various library reports

**Reports:**
- Overdue Books Report: Track books that are past their due date
- Currently Borrowed Books: See all books currently checked out
- Authors with Available Books: View authors and their available book counts

#### Frontend (Vue.js + TailwindCSS)

**Pages:**
- **Dashboard**: Home page with library statistics and overview
- **Books Management**: Full CRUD interface for books with search and filtering capabilities
- **Authors**: Manage authors with a clean interface
- **Categories**: Categorize and organize books
- **Members**: Member registration and management
- **Transactions**: Track borrowing and returning of books
- **Reports**: Generate and view various library reports

**Components:**
- **Custom Form Components**: Reusable form inputs and selects with validation
- **Modern Dialog**: Elegant modal dialogs for forms and confirmations
- **Fancy Data Table**: Feature-rich data tables with sorting, filtering and pagination
- **Navigation Components**: Header and sidebar for intuitive navigation

**Features:**
- Responsive design that works on desktop and mobile devices
- Dark/light mode support
- Real-time data updates
- Form validation and error handling
- Image upload for book covers
- Comprehensive search and filtering capabilities

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app lms
```

### Frontend Development

The frontend is built with Vue 3, Vue Router, TailwindCSS, and Frappe UI. To develop the frontend:

```bash
cd frontend
npm install
npm run dev
```

For production build:

```bash
cd frontend
npm run build
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/lms
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.

### License

MIT