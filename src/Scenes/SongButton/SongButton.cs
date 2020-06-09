using Godot;
using System.Collections.Generic;

public class SongButton : TextureButton
{

    [Export]
    public string ShybPath;

    [Export]
    public string SongName;

    [Signal]
    public delegate void Leaving();



    public override void _Ready()
    {
        GetNode<Label>("Label").Text = SongName;
    }

    public void OnPressed()
    {
        string title;
        List<PathManager.TimedPathNode>[] Moves;
        Godot.AudioStream Song;

        SongsManager.Deserialize(ShybPath, out title, out Song, out Moves);

        PackedScene target = GD.Load("res://Scenes/Play/Play.tscn") as PackedScene;
        Play scene = (Play) target.Instance();
        scene.Song = Song;
        scene.Moves = Moves;

        EmitSignal(nameof(Leaving));
        QueueFree();
        GetTree().Root.AddChild(scene);
    }

}
