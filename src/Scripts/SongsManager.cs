using System;
using Godot;
using System.Collections.Generic;
using System.IO.Compression;

public class SongsManager : Node
{
    public static string ParentPath {
        get {
            return OS.GetUserDataDir();
        }
    }

    public static List<string> List()
    {
        string song;
        List<string> songs = new List<string>();
        Directory userData = new Directory();
        userData.Open("user://");
        userData.ListDirBegin();
        while ((song = userData.GetNext()) != "") 
            if (song != "." && song != ".." && song != "mono") songs.Add(song);
        userData.ListDirEnd();
        return songs;
    }

    public static void Serialize(string title, string audioPath, List<PathManager.TimedPathNode>[] moves, bool cloneAudio = true)
    {
        // Define paths
        string tmpFolder = System.IO.Path.Combine(ParentPath, "__tmp__");
        string tmpSongPath = $"user://__tmp__/{title}.txt";
        string tmpAudioPath = System.IO.Path.Combine(ParentPath, "__tmp__", $"{title}.wav");
        string targetZip = System.IO.Path.Combine(ParentPath, $"{title}.shyb");

        // Create tmp dir
        System.IO.Directory.CreateDirectory(tmpFolder);

        // Create tmp song file
        File song = new File();
        song.Open(tmpSongPath, File.ModeFlags.Write);

        List<PathManager.TimedPathNode> noseMoves = moves[0];
        List<PathManager.TimedPathNode> rWristMoves = moves[1];
        List<PathManager.TimedPathNode> lWristMoves = moves[2];

        float[] countsLine = { noseMoves.Count, rWristMoves.Count, lWristMoves.Count };
        song.StoreLine(string.Join(":", countsLine));
        GD.Print(string.Join(":", countsLine));
        
        noseMoves.AddRange(rWristMoves);
        noseMoves.AddRange(lWristMoves);
        
        foreach (PathManager.TimedPathNode node in noseMoves)
        {
            float[] line = { node.TimeStamp, node.Position.x, node.Position.y };
            song.StoreLine(string.Join(":", line));
        }
        
        song.Close();

        // Create tmp audio file
        System.IO.File.Copy(audioPath, tmpAudioPath);

        // Zip tmp folder
        if (System.IO.File.Exists(targetZip)) System.IO.File.Delete(targetZip);
        ZipFile.CreateFromDirectory(tmpFolder, targetZip);

        // Remove tmp folder
        DeleteDirectory(tmpFolder);
    }

    public static void Deserialize(string filename, out string title, out Godot.AudioStream song, out List<PathManager.TimedPathNode>[] moves)
    {
        // Define paths
        filename = System.IO.Path.Combine(ParentPath, filename);
        title = System.IO.Path.GetFileNameWithoutExtension(filename);
        string tmpFolder = System.IO.Path.Combine(ParentPath, "__tmp__");
        string songPath = System.IO.Path.Combine(tmpFolder, $"{title}.wav");
        string movesPath = System.IO.Path.Combine(tmpFolder, $"{title}.txt");

        // Unzip to tmp folder
        ZipFile.ExtractToDirectory(filename, tmpFolder);

        // Load audiostream from song file
        song = AudioBufferFromFile(songPath);

        // Get moves
        string[] lines = System.IO.File.ReadAllLines(movesPath);
        string[] counts = lines[0].Split(":");
        int noseCount = Convert.ToInt16(counts[0]);
        int rWristCount = Convert.ToInt16(counts[1]) + noseCount;
        int lWristCount = Convert.ToInt16(counts[2]) + rWristCount;
        int index = 0;

        List<PathManager.TimedPathNode> noseMoves = new List<PathManager.TimedPathNode>();
        while (++index < noseCount)
        {
            string[] fields = lines[index].Split(":");
            float timeStamp = (float) Convert.ToDouble(fields[0]);
            float x = (float) Convert.ToDouble(fields[1]);
            float y = (float) Convert.ToDouble(fields[2]);
            noseMoves.Add(new PathManager.TimedPathNode(new Vector2(x, y), timeStamp));
        }

        List<PathManager.TimedPathNode> rWristMoves = new List<PathManager.TimedPathNode>();
        while (++index < rWristCount)
        {
            string[] fields = lines[index].Split(":");
            float timeStamp = (float) Convert.ToDouble(fields[0]);
            float x = (float) Convert.ToDouble(fields[1]);
            float y = (float) Convert.ToDouble(fields[2]);
            rWristMoves.Add(new PathManager.TimedPathNode(new Vector2(x, y), timeStamp));
        }

        List<PathManager.TimedPathNode> lWristMoves = new List<PathManager.TimedPathNode>();
        while (++index < lWristCount)
        {
            string[] fields = lines[index].Split(":");
            float timeStamp = (float) Convert.ToDouble(fields[0]);
            float x = (float) Convert.ToDouble(fields[1]);
            float y = (float) Convert.ToDouble(fields[2]);
            lWristMoves.Add(new PathManager.TimedPathNode(new Vector2(x, y), timeStamp));
        }

        moves = new List<PathManager.TimedPathNode>[] { noseMoves, rWristMoves, lWristMoves };

        // Remove tmp folder
        DeleteDirectory(tmpFolder);
    }

    // UTILS
    public static void DeleteDirectory(string target_dir)
    {
        string[] files = System.IO.Directory.GetFiles(target_dir);
        string[] dirs = System.IO.Directory.GetDirectories(target_dir);

        foreach (string file in files)
        {
            System.IO.File.SetAttributes(file, System.IO.FileAttributes.Normal);
            System.IO.File.Delete(file);
        }

        foreach (string dir in dirs)
        {
            DeleteDirectory(dir);
        }

        System.IO.Directory.Delete(target_dir, false);
    }

    public static AudioStreamSample AudioBufferFromFile(string songPath)
    {
                // Load wav buffer from song file
        File songFile = new File();
        songFile.Open(songPath, File.ModeFlags.Read);
        var buffer = songFile.GetBuffer((int) songFile.GetLen());
        songFile.Close();

        // Load audio stream from wav buffer
        AudioStreamSample stream = new AudioStreamSample();
        stream.Format = AudioStreamSample.FormatEnum.Format16Bits;
        stream.Data = buffer;
        stream.Stereo = true;
        return stream;
    }
}
