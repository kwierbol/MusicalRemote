package com.example.karolinawierbol.multipilot;

public class Song {
    private String title = "Tytuł utworu", artist = "Nazwa artysty";

    public Song(String title, String artist){
        this.artist = artist;
        this.title = title;
    }

    public String getTitle(){ return title; }
    public String getArtist() {
        return artist;
    }

    @Override
    public String toString(){
        return title + " by " + artist;
    }
}
