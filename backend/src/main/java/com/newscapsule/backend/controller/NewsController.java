package com.newscapsule.backend.controller;

import com.newscapsule.backend.model.News;
import com.newscapsule.backend.service.NewsService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/news")
public class NewsController {

    private final NewsService newsService;

    public NewsController(NewsService newsService) {
        this.newsService = newsService;
    }

    @GetMapping("/")
    public List<News> getNews() {
        return newsService.getAllNews();
    }

    @GetMapping("/{slug}/")
    public News getNewsBySlug(@PathVariable String slug) {
        return newsService.getNewsBySlug(slug);
    }

    @GetMapping("/search/{title}/")
    public List<News> searchNewsByTitle(@PathVariable String title) {
        return newsService.searchNewsByTitle(title);
    }
}
