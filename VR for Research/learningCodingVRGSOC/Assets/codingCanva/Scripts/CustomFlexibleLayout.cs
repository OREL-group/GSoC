using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace Flexalon
{
    // Custom Flexible Layout that inherits from FlexalonFlexibleLayout and adds background image and color management
    public class CustomFlexibleLayout : FlexalonFlexibleLayout
    {
        [SerializeField]
        private Sprite backgroundSprite;

        [SerializeField]
        private Color backgroundColor = Color.white;

        private Image backgroundImage;

        public override Bounds Measure(FlexalonNode node, Vector3 size, Vector3 min, Vector3 max)
        {
            // Call the base class Measure method
            var bounds = base.Measure(node, size, min, max);

            // Add any additional Measure logic here if needed

            return bounds;
        }

        public override void Arrange(FlexalonNode node, Vector3 layoutSize)
        {
            // Call the base class Arrange method
            base.Arrange(node, layoutSize);

            // Manage the background image and color
            ManageBackground(node, layoutSize);
        }

        private void ManageBackground(FlexalonNode node, Vector3 layoutSize)
        {
            if (backgroundImage == null)
            {
                // Add Image component directly to the node's GameObject if it doesn't exist
                backgroundImage = node.GameObject.GetComponent<Image>();
                if (backgroundImage == null)
                {
                    backgroundImage = node.GameObject.AddComponent<Image>();
                }
                backgroundImage.sprite = backgroundSprite;
                backgroundImage.type = Image.Type.Sliced; // or set to Simple, Tiled, etc. based on your needs
            }

            if (backgroundImage != null)
            {
                var backgroundRectTransform = backgroundImage.GetComponent<RectTransform>();
                if (backgroundRectTransform != null)
                {
                    // Ensure the background image size matches the layout size
                    backgroundRectTransform.anchorMin = new Vector2(0, 0);
                    backgroundRectTransform.anchorMax = new Vector2(1, 1);
                    backgroundRectTransform.offsetMin = Vector2.zero;
                    backgroundRectTransform.offsetMax = Vector2.zero;
                    backgroundRectTransform.localPosition = Vector3.zero;

                    // Update the background color
                    backgroundImage.color = backgroundColor;
                }
            }
        }
    }
}
