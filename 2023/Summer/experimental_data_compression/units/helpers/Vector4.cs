/// <summary>
/// Stores up to four dimensions of data for a single point.
/// </summary>
public class Vector4<T> {
    public T? x, y, z, a;

    public Vector4() {
        Assign(default, default, default, default);
    }

    public Vector4(T x) {
        Assign(x, default, default, default);
    }

    public Vector4(T x, T y) {
        Assign(x, y, default, default);
    }

    public Vector4(T x, T y, T z) {
        Assign(x, y, z, default);
    }

    public Vector4(T x, T y, T z, T a) {
        Assign(x, y, z, a);
    }

    /// <summary>
    /// Sub-constructor.
    /// </summary>
    private void Assign(T? x, T? y, T? z, T? a) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.a = a;
    }

    /// <summary>
    /// Gives the amount of dimensions that are currently being used.
    /// </summary>
    /// <returns>The number of dimensions.</returns>
    public int Dimensions() {
        int result = 0;
        if(x != null) result++;
        if(y != null) result++;
        if(z != null) result++;
        if(a != null) result++;
        return result;
    }

    public override string ToString() {
        string result = "V(";
        if(x != null) {
            result += x.ToString();
            if(y != null || z != null || a != null) result += ", ";
        }
        if(y != null) {
            result += y.ToString();
            if(z != null || a != null) result += ", ";
        }
        if(z != null) {
            result += z.ToString();
            if(a != null) result += ", ";
        }
        if(a != null) result += a.ToString();
        return result += ")";
    }
}