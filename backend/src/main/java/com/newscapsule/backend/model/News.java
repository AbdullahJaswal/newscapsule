package com.newscapsule.backend.model;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;

import java.sql.Timestamp;
import java.util.List;

@Entity
@Table(name = "news")
@NamedEntityGraph(name = "News.details", attributeNodes = @NamedAttributeNode("newsDetails"))
public class News {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "title", nullable = false)
    private String title;

    @Column(name = "title_text", nullable = false)
    private String titleText;

    @Column(name = "slug", unique = true, nullable = false)
    private String slug;

    @Column(name = "created_at", nullable = false)
    private Timestamp createdAt;

    @Column(name = "updated_at", nullable = false)
    private Timestamp updatedAt;

    @OneToMany(mappedBy = "news", cascade = CascadeType.ALL, fetch = FetchType.EAGER)
    @JsonManagedReference
    private List<NewsDetail> newsDetails;

    public News() {

    }

    public News(Long id, String title, String titleText, String slug, Timestamp createdAt, Timestamp updatedAt, List<NewsDetail> newsDetails) {
        this.id = id;
        this.title = title;
        this.titleText = titleText;
        this.slug = slug;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.newsDetails = newsDetails;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getTitleText() {
        return titleText;
    }

    public void setTitleText(String titleText) {
        this.titleText = titleText;
    }

    public String getSlug() {
        return slug;
    }

    public void setSlug(String slug) {
        this.slug = slug;
    }

    public Timestamp getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Timestamp createdAt) {
        this.createdAt = createdAt;
    }

    public Timestamp getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Timestamp updatedAt) {
        this.updatedAt = updatedAt;
    }

    public List<NewsDetail> getNewsDetails() {
        return newsDetails;
    }

    public void setNewsDetails(List<NewsDetail> newsDetails) {
        this.newsDetails = newsDetails;
    }

    @Override
    public String toString() {
        return "News[id=%d, title='%s', slug='%s', createdAt='%s', updatedAt='%s']".formatted(
                id, title, slug, createdAt, updatedAt
        );
    }
}
