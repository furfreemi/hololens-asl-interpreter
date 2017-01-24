using UnityEngine;
using UnityEngine.VR.WSA.Input;
using System.Collections;

public class PauseBehaviorScript : MonoBehaviour {

    Animation anim;
    GestureRecognizer recognizer;

    public static PauseBehaviorScript Instance { get; private set; }
 
    void Start () {
        Instance = this;
        anim = GetComponent<Animation>();
        recognizer = new GestureRecognizer();
        recognizer.TappedEvent += (source, tapCount, ray) =>
        {
            if (anim.isPlaying)
            {
                anim.Stop();
            }
            else anim.Play();
        };

        recognizer.StartCapturingGestures();
    }
	
	void Update () {
	
	}
}
