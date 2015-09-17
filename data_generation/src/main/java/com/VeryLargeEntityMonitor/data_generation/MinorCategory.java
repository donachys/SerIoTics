public class MinorCategory{
	public enum MinorType{ HALLWAY, KITCHEN, BATHROOM, STORAGE, CLASSROOM }
	MinorType type;
	public MinorCategory(MinorType mt){
		type = mt;
	}
}