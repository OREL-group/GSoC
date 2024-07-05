using UnityEngine;
using TMPro;
using Flexalon;

public class ActionLine : MonoBehaviour
{
    public TextMeshProUGUI lineNumberText;
    public FlexalonFlexibleLayout contentLayout;
    private int contentLayoutSize;

    void Start()
    {
        contentLayout = contentLayout.GetComponentInChildren<FlexalonFlexibleLayout>();
        contentLayoutSize = contentLayout.Node.Children.Count;
        UpdateLineNumber();
    }

    public void UpdateLineNumber()
    {
        lineNumberText.text = (transform.GetSiblingIndex() + 1).ToString();
    }

    public void AddItem(GameObject newItem)
    {
        newItem.transform.SetParent(contentLayout.transform, false);
        ActionLineUsage lineManager = FindObjectOfType<ActionLineUsage>();
        lineManager.CheckAndCreateNewLine(this);
    }

    public string GetActionsText()
    {
        string actionsText = "";
        foreach (Transform child in contentLayout.transform)
        {
            ActionComponent action = child.GetComponent<ActionComponent>();
            if (action != null)
            {
                actionsText += action.action.GetActionText() + "\n";
            }
        }
        return actionsText;
    }
}
