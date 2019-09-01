package com.example.karolinawierbol.multipilot;

import android.content.Context;

import java.util.*;

public class SongsQueue extends android.app.Application {

    private static SongsQueue instance;

    private int ID;
    private String pass;
    private Song previousSong = null;
    private Song currentSong = null;
    private Queue<Song> sQ;

    public SongsQueue() {

        instance = this;

        Random rand = new Random();
        this.ID = rand.nextInt(999999) + 1;

        //TODO handle passwords more securely?
        this.pass = pass;

        //initialize queue
        sQ = new LinkedList<Song>();
    }

    public static Context getContext() {
        return instance;
    }

    public static SongsQueue getInstance() {
        return instance;
    }

    public void addSong(Song s) {
        sQ.add(s);
    }

//    public void nextSong() {
//
//        if(sQ.isEmpty())
//            //TODO!!!
//            //throw new EmptySongsQueueException("Kolejka jest pusta");
//            System.out.println("Kolejka jest pusta");
//        else {
//            //the next element in line is now the current song
//            previousSong = currentSong;
//            currentSong = sQ.element(); //get first element but don't remove
//            sQ.remove();
//        }
//    }
//
//    public void prevSong(){
//
//        if(previousSong != null)
//            currentSong = previousSong;
//
//    }

    public Song getCurrentSong(){

        if(currentSong == null)
            currentSong = new Song("No current song", "No artist");
        return currentSong;
    }

    public boolean validatePass(String pass) {
        return this.pass == pass;
    }

    public boolean validateID(int ID) {
        return this.ID == ID;
    }

    public int getID() { return this.ID; }

}
