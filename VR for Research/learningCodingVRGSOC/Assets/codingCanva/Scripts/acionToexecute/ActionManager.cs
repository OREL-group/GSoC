using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using Flexalon;
using TMPro;

public class ActionManager : MonoBehaviour
{
    public FlexalonFlexibleLayout mainLayout;
    public TextMeshProUGUI outputPanel;

    void Start()
    {
        UpdateAndPrintActions();
    }

    public void UpdateAndPrintActions()
    {
        List<string> actionTexts = new List<string>();

        for (int i = 0; i < mainLayout.Node.Children.Count; i++)
        {
            ActionLine line = mainLayout.Node.Children[i].GameObject.GetComponent<ActionLine>();
            if (line != null)
            {
                foreach (Transform child in line.contentLayout.transform)
                {
                    ActionComponent actionComponent = child.GetComponent<ActionComponent>();
                    if (actionComponent != null && actionComponent.action != null)
                    {
                        actionTexts.Add(actionComponent.action.GetActionText());
                    }
                }
            }
        }

        PrintActions(actionTexts);
    }

    private void PrintActions(List<string> actions)
    {
        outputPanel.text = string.Join("\n", actions);
    }
}
