package com.example.firstapp

import android.os.AsyncTask
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.content.Intent
import android.net.Uri
import android.widget.Button
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.Socket

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activate_main)

        val button: Button = findViewById(R.id.button)
        button.setOnClickListener {
            GetRaspberryPiIpTask().execute()
        }
    }

    private inner class GetRaspberryPiIpTask : AsyncTask<Void, Void, String>() {
        override fun doInBackground(vararg params: Void?): String? {
            return try {
                val socket = Socket("192.168.137.177", 9999)
                val reader = BufferedReader(InputStreamReader(socket.getInputStream()))
                val ip = reader.readLine()
                reader.close()
                socket.close()
                ip
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }

        override fun onPostExecute(ip: String?) {
            super.onPostExecute(ip)
            if (ip != null) {
                val url = "http://$ip:5000"
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                startActivity(intent)
            }
        }
    }
}
