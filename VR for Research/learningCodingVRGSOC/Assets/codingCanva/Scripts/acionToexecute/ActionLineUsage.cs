using Flexalon;
using UnityEngine;

public class ActionLineUsage : MonoBehaviour
{
    public GameObject linePrefab; // The Line prefab containing a FlexalonFlexibleLayout and a Text item
    public FlexalonFlexibleLayout mainLayout; // The main layout containing all lines
    public bool reorderable = true; // Option to activate/deactivate reordering

    public void AddNewItem(GameObject newItem)
    {
        if (mainLayout.Node.Children.Count == 0)
        {
            CreateNewLine();
        }

        // Add the new item to the content layout of the existing last line
        FlexalonNode lastLineNode = mainLayout.Node.Children[mainLayout.Node.Children.Count - 1];
        ActionLine lastLineScript = lastLineNode.GameObject.GetComponent<ActionLine>();
        lastLineScript.AddItem(newItem);

        // Update all line numbers
        UpdateAllLineNumbers();

        // Activate draggable on children if reorderable is enabled
        if (reorderable)
        {
            ActivateDraggableOnChildren(mainLayout.gameObject);
        }
    }

    public void CheckAndCreateNewLine(ActionLine line)
    {
        // If the current line is not the last one, no need to create a new line
        if (line.transform.GetSiblingIndex() < mainLayout.Node.Children.Count - 1)
        {
            return;
        }

        // If the current line has children in the content layout, create a new line
        if (line.contentLayout.Node.Children.Count > 0)
        {
            CreateNewLine();
        }
    }

    private void CreateNewLine()
    {
        GameObject newLineObject = Instantiate(linePrefab, mainLayout.transform);
        ActionLine newLineScript = newLineObject.GetComponent<ActionLine>();
        newLineScript.UpdateLineNumber();
    }

    private void UpdateAllLineNumbers()
    {
        for (int i = 0; i < mainLayout.Node.Children.Count; i++)
        {
            ActionLine lineScript = mainLayout.Node.Children[i].GameObject.GetComponent<ActionLine>();
            lineScript.UpdateLineNumber();
        }
    }

    private void ActivateDraggableOnChildren(GameObject parentObject)
    {
        FlexalonInteractable[] interactables = parentObject.GetComponentsInChildren<FlexalonInteractable>();
        foreach (var interactable in interactables)
        {
            interactable.Draggable = true;
        }
    }
}
