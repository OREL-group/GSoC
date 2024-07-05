using UnityEngine;

public class ActionComponent : MonoBehaviour
{
    public ActionBase action;

    void Start()
    {
        if (action != null)
        {
            Debug.Log(action.GetActionText());
        }
    }
}
