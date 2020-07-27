# YouTube Haiku Compilation Bot

<p align="center">
  <a href="http://www.youtube.com/channel/UC4bbRJvsJ5ruK2znzjOOZCg?sub_confirmation=1">
    <img src="imgs/yt-haiku.png">
  </a>
</p>
<p align="left">
  <a href="http://www.youtube.com/channel/UC4bbRJvsJ5ruK2znzjOOZCg?sub_confirmation=1">
    <img src="imgs/github/subscribe.jpg", width="20%" height="30%">
  </a>
</p>

A ~~bot~~ script that creates YouTube Haiku compilations. (Planning to make it more of a *bot* in the future, for now the script is run myself). Compilations will be posted regularly to the **[YouTube channel](https://www.youtube.com/channel/UC4bbRJvsJ5ruK2znzjOOZCg)**

## YouTube Haiku?

<p align="center">
  <a href="https://www.youtube.com/watch?v=BvQ571eAOZE">
    <img src="imgs/github/gus_johnson.jpg" alt="Recording a Spotify Ad - Gus Johnson" width="448" height="252">
  </a>
</p>

YouTube Haiku is a [subreddit](https://www.reddit.com/r/youtubehaiku/) dedicated to the finest of bite-sized comedy videos. In the essence of the *Vine compilations* of my youth, this program amalgamates the best videos of a given time period and uploads them in an easy-to-consume format.

## Usage
| Option                | Type     | Description                                      |
|-----------------------|----------|--------------------------------------------------|
| -p , --period         | string   | Options: 'week', 'month', 'year', 'all time'. Default value: "week". |
| -mv , --max-vids      | int      | Max number of vids for a given compilation. Default value: 5.|
| -ms , --min-score     | int      | Min number of upvotes to get into the compilation. Default value: 0.|
| -nd, --no-download    | N/A      | Indicates to not download videos locally. Takes no argument.   |
| -tl , --time-limit    | int      | Max duration of compilation in minutes. No limit by default.|
| -y, --yes             | N/A      | Indicates an assumed "yes" response to all command line prompts  |

<br/>

**ex.** Create compilation of consisting of the top 6 posts of all time, with a time limit of 7 minutes, and a minimum score of 1000 upvotes, but don't download the videos locally (assume they are already downloaded).

```bash
python src/main.py-p "all time" -mv 6 -tl 7 -ms 1000 -nd
```
