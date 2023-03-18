import { Outlet, NavLink, Link } from "react-router-dom";

// import github from "../../assets/github.svg";
import microsoft from "../../assets/microsoft.svg"

import styles from "./Layout.module.css";

const Layout = () => {
    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer}>
                    <Link to="/" className={styles.headerTitleContainer}>
                        <h3 className={styles.headerTitle}>SolutionOps Playbook</h3>
                    </Link>
                    <nav>
                        <ul className={styles.headerNavList}>
                            <li>
                                <NavLink to="/" className={({ isActive }) => (isActive ? styles.headerNavPageLinkActive : styles.headerNavPageLink)}>
                                    Chat
                                </NavLink>
                            </li>
                            <li className={styles.headerNavLeftMargin}>
                                <a href="https://www.ms-playbook.com/" target={"_blank"} title="Microsoft Solutions Playbook">
                                    <img
                                        src={microsoft}
                                        alt="Microsoft Solutions Playbook"
                                        aria-label="Link to Microsoft Solutions Playbook"
                                        width="20px"
                                        height="20px"
                                        className={styles.microsoftLogo}
                                    />
                                </a>
                            </li>
                        </ul>
                    </nav>
                    <h4 className={styles.headerRightText}>Azure OpenAI + Chroma Vector DB</h4>
                </div>
            </header>

            <Outlet />
        </div>
    );
};

export default Layout;
