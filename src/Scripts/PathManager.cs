using System.Collections.Generic;
using Godot;

public class PathManager
{

    public struct TimedPathNode
    {
        public Vector2 Position;
        public float TimeStamp;
        public TimedPathNode(Vector2 position, float timeStamp = 0)
        {
            Position = position;
            TimeStamp = timeStamp;
        }
    }

    public static double MAX_MIDDLE_HEIGHT = 0.005;
    public static double TOO_NEAR_THRESHOLD = 0.009;

    public List<TimedPathNode> Nodes;

    public PathManager()
    {
        Nodes = new List<TimedPathNode>();
    }

    public PathManager(List<TimedPathNode> nodes)
    {
        Nodes = nodes;
    }

    public void Add(TimedPathNode node)
    {
        Nodes.Add(node);
    }

    public void AddMany(List<TimedPathNode> nodes)
    {
        Nodes.AddRange(nodes);
    }


    // ############################################################## 
    // Simplifications
    // 

    public PathManager Simplify()
    {
        RemoveZeros();
        // RemoveSameNeighbors();
        // FilterByDistance();
        // FilterByMiddleHeight();
        return this;
    }

    public void FilterByMiddleHeight()
    {
        List<TimedPathNode> nodesToRomove = new List<TimedPathNode>();

        for (int i = 1; i < Nodes.Count - 1; i += 1)
        {
            Vector2 A = Nodes[i - 1].Position;
            Vector2 B = Nodes[i + 1].Position;
            Vector2 M = Nodes[i].Position;

            double ab = A.DistanceTo(B);
            double mb = M.DistanceTo(B);
            double ma = M.DistanceTo(A);

            double p = (ab + ma + mb) / 2;
            double a = System.Math.Sqrt(p * (p - ab) * (p - ma) * (p - mb));
            double h = (ab > 0) ?  2 * a / ab : 0;

            if (h > MAX_MIDDLE_HEIGHT)
            {
                nodesToRomove.Add(Nodes[i]);
            }
        }

        foreach (TimedPathNode node in nodesToRomove)
        {
            Nodes.Remove(node);
        }
    }

    public void FilterByDistance()
    {
        List<TimedPathNode> nodesToRomove = new List<TimedPathNode>();

        for (int i = 0; i < Nodes.Count - 1; i += 1)
        {
            Vector2 A = Nodes[i].Position;
            Vector2 B = Nodes[i + 1].Position;

            double distance = A.DistanceTo(B);

            if (distance > TOO_NEAR_THRESHOLD)
            {
                nodesToRomove.Add(Nodes[i]);
            }
        }

        foreach (TimedPathNode node in nodesToRomove)
        {
            Nodes.Remove(node);
        }      
    }

    public void RemoveSameNeighbors()
    {
        List<TimedPathNode> nodesToRomove = new List<TimedPathNode>();

        for (int i = 0; i < Nodes.Count - 1; i += 1)
        {
            Vector2 A = Nodes[i].Position;
            Vector2 B = Nodes[i + 1].Position;

            if (A.x == B.x && A.y == B.y)
            {
                nodesToRomove.Add(Nodes[i]);
            }
        }

        foreach (TimedPathNode node in nodesToRomove)
        {
            Nodes.Remove(node);
        }      
    }

    public void RemoveZeros()
    {
        List<TimedPathNode> nodesToRomove = new List<TimedPathNode>();

        for (int i = 0; i < Nodes.Count; i += 1)
        {
            Vector2 A = Nodes[i].Position;

            if (A.x == 0 || A.y == 0)
            {
                nodesToRomove.Add(Nodes[i]);
            }
        }

        foreach (TimedPathNode node in nodesToRomove)
        {
            Nodes.Remove(node);
        }  
    }

}