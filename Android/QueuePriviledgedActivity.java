package com.example.karolinawierbol.multipilot;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;

public class QueuePriviledgedActivity extends AppCompatActivity {

    //GUI elements
    TextView upperTitle, lowerTitle, songTitle, artistName;
    EditText prompt;
    Button buttonSend, buttonPlay, buttonNext, buttonPrev;
    SeekBar volumeBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_queue_priviledged);

        //GUI elements initialization
        upperTitle = (TextView) findViewById(R.id.textView3);
        prompt = (EditText) findViewById(R.id.editText2);
        buttonSend = (Button) findViewById(R.id.button6);

        lowerTitle = (TextView) findViewById(R.id.textView4);
        songTitle = (TextView) findViewById(R.id.textView5);
        artistName = (TextView) findViewById(R.id.textView6);

        buttonPrev = (Button) findViewById(R.id.button8);
        buttonPlay = (Button) findViewById(R.id.button7);
        buttonNext = (Button) findViewById(R.id.button9);

        volumeBar = (SeekBar) findViewById(R.id.seekBar2);

        final SongsQueue sq = SongsQueue.getInstance();
        final BluetoothConnection2 bc2 = BluetoothConnection2.getInstance(); //wywolywane na klasie, a nie na obiekcie???

        //tutaj nowy watek do nasluchiwania?
        songTitle.setText(sq.getCurrentSong().getTitle());
        artistName.setText(sq.getCurrentSong().getArtist());

        //buttons actions

        buttonSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String msg = "NEW_SONG" + prompt.getText().toString() + "\r\n";
                prompt.setText("");
                bc2.write(msg);
                String server_answer = null;
                try {
                    server_answer = bc2.receiveData();
                } catch (IOException e) {
                    Log.i("err_recv_msg", "Error while receiving message from server");
                }

                if (server_answer.equals("NEW_SONG_ERR\r\n")) {
                    Utils.showToast(QueuePriviledgedActivity.this, "BLAD PRZY DODAWANIU PIOSENKI!");
                }
            }
        });

        buttonPrev.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                bc2.write("PREV\r\n");
            }
        });

        buttonPlay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                bc2.write("PLAY\r\n");
            }
        });

        buttonNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                bc2.write("NEXT\r\n");
            }
        });

        new Thread(new Runnable() {
            public void run() {
                Log.i("watek", "Stworzono watek aktualizujacy");

                //receiveDataContinuously
                byte[] buffer = new byte[256];
                int bytes;

                while (true) {
//                    Log.i("watek", "petla");
                    try {
                        InputStream is = bc2.getInStream();
                        bytes = is.read(buffer);
                        Log.i("watek", "instancja bajty przeczytane");

                        String readMessage = new String(buffer, 0, bytes);
                        readMessage = bc2.decodeString(readMessage);
                        Log.i("watek", readMessage);
//
//                        String[] parts = readMessage.split("_");
//                        String firstPart = parts[0]; //protocol message
//                        if (firstPart.equals("CURRENT") && parts.length == 3){
//                            songTitle.setText(parts[1]);
//                            artistName.setText(parts[2]);
                        }
                        catch(Exception e) {
//                    } catch (IOException e) {
//                        Log.i("errorRECVINSIDE", "Error receiving inside method");
//                        break;
                    }
                }
            }
        }).start();

    }
}
