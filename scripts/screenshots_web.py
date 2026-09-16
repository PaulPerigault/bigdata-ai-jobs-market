"""Captures des interfaces web (HDFS NameNode, Jupyter) pour report/figures/.

Recette : `task screenshots-web` (dépend de `task up`). Playwright en
mode headless, aucune session authentifiée (voir CLAUDE.md — les
captures GitHub authentifiées restent manuelles, cf. section captures).
"""

import os
import time

from playwright.sync_api import sync_playwright

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "report", "figures")
JUPYTER_TOKEN = os.environ.get("JUPYTER_TOKEN", "bigdata")


def capture(page, url, out_name, wait_selector=None, wait_ms=500):
    page.goto(url, wait_until="networkidle")
    if wait_selector:
        page.wait_for_selector(wait_selector, timeout=15000)
    time.sleep(wait_ms / 1000)
    path = os.path.join(FIGURES_DIR, out_name)
    page.screenshot(path=path, full_page=True)
    print(f"WROTE {path}")


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        # HDFS NameNode : arborescence /projet_ia (raw + processed).
        capture(
            page,
            "http://localhost:50070/explorer.html#/projet_ia",
            "etape2_hdfs_namenode_explorer.png",
            wait_selector="#panel table tbody tr",
        )

        # Jupyter : notebook du projet ouvert dans l'environnement du
        # conteneur. Le dashboard final (issue #96) n'existe pas encore
        # — cette capture montre l'environnement connecté à la stack,
        # pas le dashboard fini (à recapturer une fois #96 fait).
        capture(
            page,
            f"http://localhost:8888/notebooks/work/Analyse_Marche_Emploi_IA_PySpark.ipynb?token={JUPYTER_TOKEN}",
            "etape2_jupyter_notebook.png",
            wait_selector=".jp-Notebook, #notebook-container",
            wait_ms=1500,
        )

        browser.close()


if __name__ == "__main__":
    main()
