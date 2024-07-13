package com.newscapsule.backend.model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;

import java.sql.Timestamp;

@Entity
@Table(name = "news_detail")
public class NewsDetail {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "summary")
    private String summary;

    @Column(name = "description")
    private String description;

    @Column(name = "thumbnail")
    private String thumbnail;

    @Column(name = "image")
    private String image;

    @Column(name = "timestamp")
    private Timestamp timestamp;

    @Column(name = "url")
    private String url;

    @Column(name = "created_at", nullable = false)
    private Timestamp createdAt;

    @Column(name = "updated_at", nullable = false)
    private Timestamp updatedAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "news_id")
    @JsonBackReference
    private News news;

    public NewsDetail() {

    }

    public NewsDetail(
            Long id,
            String summary,
            String description,
            String thumbnail,
            String image,
            Timestamp timestamp,
            String url,
            Timestamp createdAt,
            Timestamp updatedAt,
            News news
    ) {
        this.id = id;
        this.summary = summary;
        this.description = description;
        this.thumbnail = thumbnail;
        this.image = image;
        this.timestamp = timestamp;
        this.url = url;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.news = news;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getThumbnail() {
        return thumbnail;
    }

    public void setThumbnail(String thumbnail) {
        this.thumbnail = thumbnail;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    public Timestamp getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Timestamp timestamp) {
        this.timestamp = timestamp;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
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

    public News getNews() {
        return news;
    }

    public void setNews(News news) {
        this.news = news;
    }

    @Override
    public String toString() {
        return "NewsDetail[id=%d, summary='%s', timestamp='%s', createdAt='%s', updatedAt='%s']".formatted(
                id, summary, timestamp, createdAt, updatedAt
        );
    }
}
