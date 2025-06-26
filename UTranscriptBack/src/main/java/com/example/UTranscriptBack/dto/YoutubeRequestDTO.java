package com.example.UTranscriptBack.dto;

public class YoutubeRequestDTO {
    private String video_url;

    public YoutubeRequestDTO() {}

    public YoutubeRequestDTO(String video_url) {
        this.video_url = video_url;
    }

    public String getVideo_url() {
        return video_url;
    }

    public void setVideo_url(String video_url) {
        this.video_url = video_url;
    }
}
