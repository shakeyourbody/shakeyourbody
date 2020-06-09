using Godot;
using System;
using System.Collections.Generic;

public class Menu : Control
{
    private List<TextureButton> _Buttons;
    private string _SongPath;
    private string _MovesPath;

    public override void _Ready()
    {
        CallDeferred(nameof(_LoadButtons));
        OS.WindowFullscreen = false;
    }

    private void _LoadButtons()
    {
        _CreateButtons();

        VBoxContainer container = GetNode<VBoxContainer>("ColorRect/VBoxContainer");
        for (int i = 0; i < container.GetChildCount(); i += 1) container.RemoveChild(container.GetChild(i));
        foreach (TextureButton button in _Buttons)
        {
            CenterContainer center = new CenterContainer();
            center.AddChild(button);
            container.AddChild(center);
        }
    }

    private void _CreateButtons()
    {
        _Buttons = new List<TextureButton>();
        List<string> files = SongsManager.List();
        GetNode<CenterContainer>("ColorRect/NoSongs").Hide();
        if (files.Count <= 0) GetNode<CenterContainer>("ColorRect/NoSongs").Show();
        else foreach (string file in files) _CreateButton(file, System.IO.Path.GetFileNameWithoutExtension(file));
    }

    private void _CreateButton(string path, string name)
    {
        PackedScene SongButton = GD.Load("res://Scenes/SongButton/SongButton.tscn") as PackedScene;
        SongButton button = (SongButton) SongButton.Instance();
        button.Connect("mouse_entered", this, nameof(OnButtonMouseEnter));
        button.Connect("Leaving", this, nameof(Cleanup));
        button.SongName = name.ToUpper();
        button.ShybPath = path;
        _Buttons.Add((TextureButton) button);
    }

    public void OnButtonMouseEnter()
    {
        GetNode<AudioStreamPlayer>("AudioStreamPlayer").Play();
    }

    public void OnSideMouseEnteredTop()
    {
        GetNode<TextureRect>("ColorRect/TextureRect").Texture = GD.Load("res://Assets/HUD/Side/hoverTop.svg") as Texture;
        OnButtonMouseEnter();

    }public void OnSideMouseEnteredBottom()
    {
        GetNode<TextureRect>("ColorRect/TextureRect").Texture = GD.Load("res://Assets/HUD/Side/hoverBottom.svg") as Texture;
        OnButtonMouseEnter();
    }

    public void OnSideMouseExited()
    {
        GetNode<TextureRect>("ColorRect/TextureRect").Texture = GD.Load("res://Assets/HUD/Side/normal.svg") as Texture;
    }


    public void Register()
    {
        GetNode<FileDialog>("RegisterDialog").PopupCentered();
    }

    public void Import()
    {
        GetNode<FileDialog>("ImportDialog").PopupCentered();
    }

    public void OnRegisterSelected(string path)
    {
        Cleanup();
        PackedScene target = GD.Load("res://Scenes/Register/Register.tscn") as PackedScene;
        Register scene = (Register) target.Instance();
        scene.SongPath = path;
        GetTree().Root.AddChild(scene);
    }

    public void OnImportSelected(string path)
    {
        string targetPath = SongsManager.ParentPath;
        string targetFile = System.IO.Path.Combine(targetPath, System.IO.Path.GetFileName(path));
        System.IO.File.Copy(path, targetFile, true);
        _LoadButtons();
    }

    public void Cleanup()
    {
        for (int i = 0; i < GetChildCount(); i += 1) GetChild(i).QueueFree();
    }
}