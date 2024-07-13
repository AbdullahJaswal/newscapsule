package com.newscapsule.backend.service;

import com.newscapsule.backend.model.News;
import com.newscapsule.backend.repository.NewsRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NewsService {

    private final NewsRepository newsRepository;

    public NewsService(NewsRepository newsRepository) {
        this.newsRepository = newsRepository;
    }

    public List<News> getAllNews() {
        return newsRepository.findAllByOrderByCreatedAtDesc();
    }

    public News getNewsBySlug(String slug) {
        return newsRepository.findBySlug(slug);
    }

    public List<News> searchNewsByTitle(String title) {
        return newsRepository.findByTitleContainingIgnoreCase(title);
    }
}
