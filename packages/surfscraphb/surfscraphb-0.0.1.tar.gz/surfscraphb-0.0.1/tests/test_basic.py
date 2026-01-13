from surfscraphp import scrape_surf_report
import os


def test_scrape_creates_csv(tmp_path):
    url = "https://www.surf-report.com/meteo-surf/carcans-plage-s1013.html"
    output = tmp_path / "test.csv"

    df = scrape_surf_report(url, output)

    assert os.path.exists(output)
    assert not df.empty
    
if __name__ == "__main__":
    test_scrape_creates_csv()