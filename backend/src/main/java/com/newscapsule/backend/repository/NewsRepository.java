package com.newscapsule.backend.repository;

import com.newscapsule.backend.model.News;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface NewsRepository extends JpaRepository<News, Long> {

    @EntityGraph(value = "News.details", type = EntityGraph.EntityGraphType.LOAD)
    List<News> findAllByOrderByCreatedAtDesc();

    @EntityGraph(value = "News.details", type = EntityGraph.EntityGraphType.LOAD)
    News findBySlug(String slug);

    @EntityGraph(value = "News.details", type = EntityGraph.EntityGraphType.LOAD)
    List<News> findByTitleContainingIgnoreCase(String title);
}
