using System;
using Godot;

public class DisplayScore : Node
{

    private static Color IColor(int r, int g, int b) 
    {
        return new Color(r/255f,g/255f,b/255f);
    }
    

    [Export]
    public string Score = "--";

    [Export]
    public Color[] BGColors = {
        IColor(251, 72, 73),
        IColor(12, 170, 255),
        new Color("7122fa"),
        new Color("560a86"),
        new Color("ff2181"),
        new Color("b76cfd"),
        new Color("02b8a2"),
        new Color("7122fa"),
        new Color("037a90"),
        new Color("fe6b35"),
        new Color("ff822e"),
    };

    public override void _Ready()
    {
        GetNode<Label>("MarginContainer/VBoxContainer/CenterContainer/VBoxContainer/Label").Text = $"{Score}%";

        Random r = new Random();
        GetNode<ColorRect>("bg").Color = BGColors[r.Next(BGColors.Length)];
    }

    public void ToMenu()
    {
        for (int i = 0; i < GetChildCount(); i += 1) GetChild(i).QueueFree();
        QueueFree();
        GetTree().ChangeScene("res://Scenes/Menu/Menu.tscn");
    }

    public void PlayPop()
    {
        GetNode<AudioStreamPlayer>("PopPlayer").Play();
    }
}
