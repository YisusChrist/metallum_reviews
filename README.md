<p align="center">
    <a href="https://github.com/YisusChrist/metallum_reviews/issues">
        <img src="https://img.shields.io/github/issues/YisusChrist/metallum_reviews?color=171b20&label=Issues%20%20&logo=gnubash&labelColor=e05f65&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/metallum_reviews/forks">
        <img src="https://img.shields.io/github/forks/YisusChrist/metallum_reviews?color=171b20&label=Forks%20%20&logo=git&labelColor=f1cf8a&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/metallum_reviews/stargazers">
        <img src="https://img.shields.io/github/stars/YisusChrist/metallum_reviews?color=171b20&label=Stargazers&logo=octicon-star&labelColor=70a5eb">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/metallum_reviews/actions">
        <img alt="Tests Passing" src="https://github.com/YisusChrist/metallum_reviews/actions/workflows/github-code-scanning/codeql/badge.svg">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/metallum_reviews/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/YisusChrist/metallum_reviews?color=0088ff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://opensource.org/license/gpl-2-0/">
        <img alt="License" src="https://img.shields.io/github/license/YisusChrist/metallum_reviews?color=0088ff">
    </a>
</p>

<br>

<p align="center">
    <a href="https://github.com/YisusChrist/metallum_reviews/issues/new?assignees=YisusChrist&labels=bug&projects=&template=bug_report.yml">Report Bug</a>
    ·
    <a href="https://github.com/YisusChrist/metallum_reviews/issues/new?assignees=YisusChrist&labels=feature&projects=&template=feature_request.yml">Request Feature</a>
    ·
    <a href="https://github.com/YisusChrist/metallum_reviews/issues/new?assignees=YisusChrist&labels=question&projects=&template=question.yml">Ask Question</a>
    ·
    <a href="https://github.com/YisusChrist/metallum_reviews/security/policy#reporting-a-vulnerability">Report security bug</a>
</p>

<br>

`metallum_reviews` is a Python package that allows you to retrieve user reviews and ratings of albums from the [Metal Archives](https://www.metal-archives.com) website. The package uses the [Enmet](https://github.com/lukjak/enmet) project to search for albums and retrieve their reviews. It is designed to be simple and easy to use, providing a straightforward way to access the reviews of your favorite albums.

<details>
<summary>Table of Contents</summary>

-   [Requirements](#requirements)
-   [Installation](#installation)
    -   [From PyPI](#from-pypi)
    -   [Manual installation](#manual-installation)
    -   [Uninstall](#uninstall)
-   [Usage](#usage)
-   [License](#license)
-   [Credits](#credits)

</details>

## Requirements

Here's a breakdown of the packages needed and their versions:

-   [poetry](https://pypi.org/project/poetry) >= 1.7.1 (_only for manual installation_)
-   [beautifulsoup4](https://pypi.org/project/beautifulsoup4) >= 4.12.3
-   [enmet](https://pypi.org/project/enmet) >= 0.9.1
-   [fake-useragent](https://pypi.org/project/fake-useragent) >= 1.5.1
-   [pyfiglet](https://pypi.org/project/pyfiglet) >= 1.0.2
-   [requests-cache](https://pypi.org/project/requests-cache) >= 1.2.1
-   [rich](https://pypi.org/project/rich) >= 13.7.1

> [!NOTE]
> The software has been developed and tested using Python `3.12.4`. The minimum required version to run the software is Python 3.6. Although the software may work with previous versions, it is not guaranteed.

## Installation

### From PyPI

`metallum_reviews` can be installed easily as a PyPI package. Just run the following command:

```bash
pip3 install metallum_reviews
```

> [!IMPORTANT]
> For best practices and to avoid potential conflicts with your global Python environment, it is strongly recommended to install this program within a virtual environment. Avoid using the --user option for global installations. We highly recommend using [pipx](https://pypi.org/project/pipx) for a safe and isolated installation experience. Therefore, the appropriate command to install `metallum_reviews` would be:
>
> ```bash
> pipx install metallum_reviews
> ```

The program can now be ran from a terminal with the `metallum_reviews` command.

### Manual installation

If you prefer to install the program manually, follow these steps:

> [!WARNING]
> This will install the version from the latest commit, not the latest release.

1. Download the latest version of [metallum_reviews](https://github.com/YisusChrist/metallum_reviews) from this repository:

    ```bash
    git clone https://github.com/YisusChrist/metallum_reviews
    cd metallum_reviews
    ```

2. Install the package:

    ```bash
    poetry install --only-main
    ```

3. Run the program:

    ```bash
    poetry run metallum_reviews
    ```

### Uninstall

If you installed it from PyPI, you can use the following command:

```bash
pipx uninstall metallum_reviews
```

## Usage

Thanks to the [Enmet](https://github.com/lukjak/enmet) project, we are able to search effortlessly albums in the [Metal Archives](https://www.metal-archives.com) website like in the following example:

```python
import enmet

results = enmet.search_albums(
    name="The Number of the Beast",
    band="Iron Maiden",
)

for album in results:
    print(album, "-", album.type)
```

The `results` variable will contain a list of albums that match the search criteria. The code will output:

```
The Number of the Beast (1982) - ReleaseTypes.FULL
The Number of the Beast (1982) - ReleaseTypes.SINGLE
Run to the Hills / The Number of the Beast (1990) - ReleaseTypes.EP
The Number of the Beast / Beast over Hammersmith (2022) - ReleaseTypes.COMPILATION
```

With this approach, we can retrieve most of the album information, except for the user reviews. Therefore, this project is not intended to replace the official Metal Archives website, but to provide a simple way to search for public reviews and ratings of albums.

The application will search for all the available reviews under the page of the album specified. The following example demonstrates how to retrieve the reviews of the album "The Number of the Beast" by Iron Maiden:

```python
import enmet
from metallum_reviews.utils import fetch_reviews


results = enmet.search_albums(
    name="The Number of the Beast",
    band="Iron Maiden",
)

# session can be a requests.Session or a requests_cache.CachedSession object
reviews = fetch_reviews(session, results, total_results)
```

The `reviews` variable will contain a list of `Review` objects, which contain the following attributes:

| Attribute | Description              | Type        |
| --------- | ------------------------ | ----------- |
| `title`   | The title of the review  | str         |
| `rating`  | The rating of the review | int         |
| `author`  | The author of the review | User        |
| `date`    | The date of the review   | datetime    |
| `content` | The text of the review   | str         |
| `album`   | The album of the review  | enmet.Album |
| `url`     | The URL of the review    | str         |

As a result, the code will output:

```
<Review: 'The Beginning Of A New Age' (82%) by Legolion17 (https://www.metal-archives.com/users/Legolion17) on 2024-06-01 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/Legolion17)>
<Review: 'IRON MAIDEN - The Number of the Beast' (95%) by K1LleRxINstiNcT (https://www.metal-archives.com/users/K1LleRxINstiNcT) on 2024-05-24 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/K1LleRxINstiNcT)>
<Review: 'Iron Maiden in 4 paragraphs' (82%) by Annable Courts (https://www.metal-archives.com/users/Annable%20Courts) on 2023-11-09 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/Annable_Courts)>
<Review: 'THE ONE for you and me' (100%) by Xyrth (https://www.metal-archives.com/users/Xyrth) on 2022-03-28 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/Xyrth)>
<Review: 'Six! Six six! The Number of the Beast!' (100%) by Slater922 (https://www.metal-archives.com/users/Slater922) on 2022-03-22 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/Slater922)>
<Review: 'Often overrated, often underestimated' (100%) by agogogt (https://www.metal-archives.com/users/agogogt) on 2021-11-28 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/agogogt)>
<Review: 'Electrifying!!' (100%) by AxlFuckingRose (https://www.metal-archives.com/users/AxlFuckingRose) on 2021-11-28 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/AxlFuckingRose)>
<Review: 'The great consolidation' (100%) by Darley (https://www.metal-archives.com/users/Darley) on 2021-11-13 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/Darley)>
<Review: 'Iron Maiden III : Satan's Work is Done' (95%) by DanielG06 (https://www.metal-archives.com/users/DanielG06) on 2021-03-14 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/DanielG06)>
<Review: 'You Better Scratch Me, From Your Black Book' (85%) by Sweetie (https://www.metal-archives.com/users/Sweetie) on 2020-03-15 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/Sweetie)>
<Review: 'This is the Iron Maiden I love' (90%) by DMhead777 (https://www.metal-archives.com/users/DMhead777) on 2019-06-20 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/DMhead777)>
<Review: 'Bloated Meandering Filler' (50%) by CuddlySilverback (https://www.metal-archives.com/users/CuddlySilverback) on 2018-07-28 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/CuddlySilverback)>
<Review: 'The score is meaningless' (87%) by gasmask_colostomy (https://www.metal-archives.com/users/gasmask_colostomy) on 2017-12-27 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/gasmask_colostomy)>
<Review: 'Oblivion Beckons Us All' (98%) by CHAIRTHROWER (https://www.metal-archives.com/users/CHAIRTHROWER) on 2017-10-02 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/CHAIRTHROWER)>
<Review: 'The Greatest Album That I Would Call Overrated' (98%) by Caleb9000 (https://www.metal-archives.com/users/Caleb9000) on 2017-07-14 00:00:00 (https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/Caleb9000)>
...
```

You can access each property of the `Review` object by using the dot notation. For example, to print the title of the first review, you can use:

```python
print(reviews[0].title)
```

The code will output:

```
The Beginning Of A New Age
```

Or you can print the full review information in a beautiful format thanks to the [rich](https://pypi.org/project/rich) text formatting library:

```python
from rich import print

print(reviews[0].full_info())
```

The code will output:

```
Title: The Beginning Of A New Age
Rating: 82%
Author: Legolion17 (https://www.metal-archives.com/users/Legolion17)
Date: 2024-06-01 00:00:00
Album: The Number of the Beast (1982)
URL: https://www.metal-archives.com/reviews/Iron_Maiden/The_Number_of_the_Beast/75/Legolion17
Content: The Number Of The Beast is one of the most influential albums in all of metal history, consistently ranked as one of the best metal albums of all time. This album is considered a classic by many, and important by all. However, it does have its own downfalls and imperfections, as most albums do. Let's dig into those.

The Number Of The Beast is remembered primarily for four reasons. 1). It is the first album Bruce Dickinson sang on with Iron Maiden, and would usher in a new era of Iron Maiden. 2). This album contains three of Iron Maiden's biggest songs, and staples to almost every live performance of theirs (The Number Of The Beast, Run To The Hills, Hallowed Be Thy Name). 3). The artwork is one of the most iconic album covers in the history of heavy metal, perhaps rivaled only by Metallica's Master Of Puppets. And 4). The boycotts and allegations of Iron Maiden being a satanic band. All of these factors make for an album to catch the eye of anyone looking to get into metal music, and all adding to the legacy of Iron Maiden.

The tracks of the albums aren't the most consistent, especially when compared to the following albums. While tracks like The Number Of The Beast and Hallowed Be Thy Name are well crafted and rightly regarded as being absolute classics, songs like Invaders and Gangland could've used a little more time in the oven. And as much as I love Run To The Hills, it's totally overrated. I'd rather they take that song out of their setlist and replace it with Children Of The Damned or 22 Acacia Avenue. Luckily, they'd step up in the quality and consistency of their albums on the following releases. This is not necessarily a bad album, but compared to some of the masterpieces Iron Maiden would put out later, this album definitely feels a little bit lower in terms of quality. It would definitely benefit from a stronger lineup, as most of the time you're going from a real good song to a merely okay one following. However, the mixing and tone of the album is excellent, with Bruce Dickinson's vocals soaring over the melodies, the guitars having that clean feel that classic metal is so well known for, a loud thundering bass guitar and drums that just fit what needs to be done to keep the album going. If you're looking for the stereotypical NWOBHM sound, this album is probably the best example of the genre.

This album is a classic, and while I believe it was important for the broader scope of metal, I feel this album does get overrated a lot. I would recommend the following two albums (1983's Piece Of Mind and 1984's Powerslave) to newer adventurers into the genre, as both those albums are bona fide masterpieces. And despite the criticism I give this album, it's still a good time with some excellent tracks, one I'll put on every once in a while.


Important Tracks:

Children Of The Damned
22 Acacia Avenue
Number Of The Beast
Hallowed Be Thy Name
```

## License

`metallum_reviews` is released under the [GPL-3.0 License](https://opensource.org/license/gpl-3-0).

## Credits

> [!NOTE]
> Thanks to [lukjak](https://github.com/lukjak) for the fantastic [Enmet](https://github.com/lukjak/enmet) project, which is used to search for albums in the Metal Archives website.
