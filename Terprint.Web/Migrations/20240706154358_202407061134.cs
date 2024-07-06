using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Terprint.Web.Migrations
{
    /// <inheritdoc />
    public partial class _202407061134 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Rating_Batch_BatchId",
                table: "Rating");

            migrationBuilder.DropForeignKey(
                name: "FK_Rating_RatingCategory_RatingCategoryId",
                table: "Rating");

            migrationBuilder.DropTable(
                name: "THCLevels");

            migrationBuilder.DropColumn(
                name: "BuyAgain",
                table: "Rating");

            migrationBuilder.DropColumn(
                name: "Effect",
                table: "Rating");

            migrationBuilder.DropColumn(
                name: "Taste",
                table: "Rating");

            migrationBuilder.RenameColumn(
                name: "RatingCategoryId",
                table: "Rating",
                newName: "RatingCategoryID");

            migrationBuilder.RenameColumn(
                name: "BatchId",
                table: "Rating",
                newName: "BatchID");

            migrationBuilder.RenameColumn(
                name: "OverallRating",
                table: "Rating",
                newName: "Value");

            migrationBuilder.RenameIndex(
                name: "IX_Rating_RatingCategoryId",
                table: "Rating",
                newName: "IX_Rating_RatingCategoryID");

            migrationBuilder.RenameIndex(
                name: "IX_Rating_BatchId",
                table: "Rating",
                newName: "IX_Rating_BatchID");

            migrationBuilder.AddColumn<string>(
                name: "RatingCategoryType",
                table: "RatingCategory",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AlterColumn<int>(
                name: "RatingCategoryID",
                table: "Rating",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AlterColumn<int>(
                name: "BatchID",
                table: "Rating",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AddColumn<int>(
                name: "Growerid",
                table: "Rating",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.CreateTable(
                name: "THCValues",
                columns: table => new
                {
                    THCValueId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    BatchID = table.Column<int>(type: "int", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Value = table.Column<double>(type: "float", nullable: false),
                    Scale = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_THCValues", x => x.THCValueId);
                    table.ForeignKey(
                        name: "FK_THCValues_Batch_BatchID",
                        column: x => x.BatchID,
                        principalTable: "Batch",
                        principalColumn: "BatchId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_THCValues_BatchID",
                table: "THCValues",
                column: "BatchID");

            migrationBuilder.AddForeignKey(
                name: "FK_Rating_Batch_BatchID",
                table: "Rating",
                column: "BatchID",
                principalTable: "Batch",
                principalColumn: "BatchId",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_Rating_RatingCategory_RatingCategoryID",
                table: "Rating",
                column: "RatingCategoryID",
                principalTable: "RatingCategory",
                principalColumn: "RatingCategoryId",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Rating_Batch_BatchID",
                table: "Rating");

            migrationBuilder.DropForeignKey(
                name: "FK_Rating_RatingCategory_RatingCategoryID",
                table: "Rating");

            migrationBuilder.DropTable(
                name: "THCValues");

            migrationBuilder.DropColumn(
                name: "RatingCategoryType",
                table: "RatingCategory");

            migrationBuilder.DropColumn(
                name: "Growerid",
                table: "Rating");

            migrationBuilder.RenameColumn(
                name: "RatingCategoryID",
                table: "Rating",
                newName: "RatingCategoryId");

            migrationBuilder.RenameColumn(
                name: "BatchID",
                table: "Rating",
                newName: "BatchId");

            migrationBuilder.RenameColumn(
                name: "Value",
                table: "Rating",
                newName: "OverallRating");

            migrationBuilder.RenameIndex(
                name: "IX_Rating_RatingCategoryID",
                table: "Rating",
                newName: "IX_Rating_RatingCategoryId");

            migrationBuilder.RenameIndex(
                name: "IX_Rating_BatchID",
                table: "Rating",
                newName: "IX_Rating_BatchId");

            migrationBuilder.AlterColumn<int>(
                name: "RatingCategoryId",
                table: "Rating",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AlterColumn<int>(
                name: "BatchId",
                table: "Rating",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AddColumn<bool>(
                name: "BuyAgain",
                table: "Rating",
                type: "bit",
                nullable: false,
                defaultValue: false);

            migrationBuilder.AddColumn<int>(
                name: "Effect",
                table: "Rating",
                type: "int",
                nullable: true);

            migrationBuilder.AddColumn<int>(
                name: "Taste",
                table: "Rating",
                type: "int",
                nullable: true);

            migrationBuilder.CreateTable(
                name: "THCLevels",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    BatchId = table.Column<int>(type: "int", nullable: true),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Scale = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Value = table.Column<double>(type: "float", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_THCLevels", x => x.Id);
                    table.ForeignKey(
                        name: "FK_THCLevels_Batch_BatchId",
                        column: x => x.BatchId,
                        principalTable: "Batch",
                        principalColumn: "BatchId");
                });

            migrationBuilder.CreateIndex(
                name: "IX_THCLevels_BatchId",
                table: "THCLevels",
                column: "BatchId");

            migrationBuilder.AddForeignKey(
                name: "FK_Rating_Batch_BatchId",
                table: "Rating",
                column: "BatchId",
                principalTable: "Batch",
                principalColumn: "BatchId");

            migrationBuilder.AddForeignKey(
                name: "FK_Rating_RatingCategory_RatingCategoryId",
                table: "Rating",
                column: "RatingCategoryId",
                principalTable: "RatingCategory",
                principalColumn: "RatingCategoryId");
        }
    }
}
