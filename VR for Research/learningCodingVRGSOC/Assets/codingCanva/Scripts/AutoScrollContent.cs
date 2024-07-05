using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class AutoScrollContent : MonoBehaviour
{
    public ScrollRect scrollRect; // Assurez-vous d'assigner votre ScrollRect dans l'inspecteur
    public float scrollSpeed = 10f; // Vitesse de défilement
    public float edgeThreshold = 50f; // Distance par rapport au bord pour commencer à défiler

    private RectTransform contentRect;
    private RectTransform viewportRect;

    void Start()
    {
        contentRect = scrollRect.content;
        viewportRect = scrollRect.viewport;
    }

    void Update()
    {
        Vector2 localMousePos;
        RectTransformUtility.ScreenPointToLocalPointInRectangle(contentRect, Input.mousePosition, null, out localMousePos);

        bool isScrolling = false;

        // Vérifie si l'objet est proche du bord du bas
        if (localMousePos.y < -contentRect.rect.height / 2 + edgeThreshold)
        {
            scrollRect.verticalNormalizedPosition -= scrollSpeed * Time.deltaTime / contentRect.rect.height;
            isScrolling = true;
        }

        // Vérifie si l'objet est proche du bord du haut
        if (localMousePos.y > contentRect.rect.height / 2 - edgeThreshold)
        {
            scrollRect.verticalNormalizedPosition += scrollSpeed * Time.deltaTime / contentRect.rect.height;
            isScrolling = true;
        }

        // Vérifie si l'objet est proche du bord gauche
        if (localMousePos.x < -contentRect.rect.width / 2 + edgeThreshold)
        {
            scrollRect.horizontalNormalizedPosition -= scrollSpeed * Time.deltaTime / contentRect.rect.width;
            isScrolling = true;
        }

        // Vérifie si l'objet est proche du bord droit
        if (localMousePos.x > contentRect.rect.width / 2 - edgeThreshold)
        {
            scrollRect.horizontalNormalizedPosition += scrollSpeed * Time.deltaTime / contentRect.rect.width;
            isScrolling = true;
        }

        // Assurez-vous que la position de défilement reste entre 0 et 1
        scrollRect.verticalNormalizedPosition = Mathf.Clamp(scrollRect.verticalNormalizedPosition, 0, 1);
        scrollRect.horizontalNormalizedPosition = Mathf.Clamp(scrollRect.horizontalNormalizedPosition, 0, 1);
    }
}
