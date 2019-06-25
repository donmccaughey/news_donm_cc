fetch('/data/news.json')
    .then(function (response) {
        return response.json();
    })
    .then(function (news) {
        var story_count = document.querySelector('#story_count');
        story_count.innerText = news.stories.length;

        var modified_date = document.querySelector('#modified_date');
        modified_date.innerText = news.modified_date;

        var list = document.querySelector('#stories_list');
        for (story of news.stories) {
            var link = document.createElement('a');
            link.href = story.link;
            link.innerText = story.title;

            var item = document.createElement('li');
            item.appendChild(link);

            list.appendChild(item);
        }
    })
    .catch(function (error) {
        console.log('Error: ' + error);
    });

